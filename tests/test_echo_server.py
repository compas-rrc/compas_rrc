from __future__ import absolute_import, division, print_function

import queue
import socket
import socketserver
import struct
import threading
import time
from copy import copy
from functools import partial

VERBOSE = True


class WireProtocol(object):
    VERSION = 4
    BYTE_ORDER = '<'
    FIXED_HEADER_LEN = 16
    HEADER_FORMAT = '4I'
    MAX_STRING_VALUES = 5
    MAX_FLOAT_VALUES = 30

    @classmethod
    def deserialize(cls, header, payload):
        sequence_id, = struct.unpack(
            cls.BYTE_ORDER + 'I', payload[0:4])
        exec_level, = struct.unpack(
            cls.BYTE_ORDER + 'I', payload[4:8])
        instruction_len, = struct.unpack(
            cls.BYTE_ORDER + 'I', payload[8:12])
        start_pos = 12

        # Read instruction
        instruction, = struct.unpack(cls.BYTE_ORDER + str(instruction_len) + 's', payload[start_pos:start_pos + instruction_len])
        start_pos += instruction_len

        # Read feedback message
        feedback_level, = struct.unpack(
            cls.BYTE_ORDER + 'I', payload[start_pos:start_pos + 4])
        start_pos += 4
        feedback_len, = struct.unpack(
            cls.BYTE_ORDER + 'I', payload[start_pos:start_pos + 4])
        start_pos += 4
        feedback, = struct.unpack(cls.BYTE_ORDER + str(feedback_len) + 's', payload[start_pos:start_pos + feedback_len])
        start_pos += feedback_len

        # Read feedback ID
        feedback_id, = struct.unpack(
            cls.BYTE_ORDER + 'I', payload[start_pos:start_pos + 4])
        start_pos += 4

        # Read string values
        string_values = []
        string_value_count, = struct.unpack(
            cls.BYTE_ORDER + 'I', payload[start_pos:start_pos + 4])
        start_pos += 4

        for _ in range(string_value_count):
            str_len, = struct.unpack(cls.BYTE_ORDER + 'I', payload[start_pos:start_pos + 4])
            start_pos += 4
            string_value, = struct.unpack(cls.BYTE_ORDER + str(str_len) + 's', payload[start_pos:start_pos + str_len])
            string_values.append(string_value)
            start_pos += str_len

        # Read float values
        float_value_count, = struct.unpack(cls.BYTE_ORDER + 'I', payload[start_pos:start_pos + 4])
        float_value_count = int(float_value_count)
        start_pos += 4
        float_format = '%df' % float_value_count
        float_values = struct.unpack(cls.BYTE_ORDER + float_format, payload[start_pos:])

        return dict(instruction=instruction,
                    sequence_id=sequence_id,
                    exec_level=exec_level,
                    feedback_level=feedback_level,
                    feedback=feedback,
                    feedback_id=feedback_id,
                    string_values=string_values,
                    float_values=float_values)


    @classmethod
    def serialize(cls, message):
        ticks = time.time()
        sec = int(ticks)
        nsec = int((ticks - int(ticks)) * 1000)

        instruction = message['instruction']
        exec_level = message['exec_level']
        feedback_level = message['feedback_level']
        feedback = message['feedback'] or ''
        feedback_id = message['feedback_id']
        string_values = message['string_values']
        float_values = message['float_values']

        # Build command
        payload_format = '3I{}s2I{}sI'.format(len(instruction), len(feedback))
        payload = [message['sequence_id'], exec_level, len(instruction), instruction, feedback_level, len(feedback), feedback, feedback_id]

        # Build string values
        current_items = len(string_values)

        if current_items > cls.MAX_STRING_VALUES:
            raise ValueError('Protocol does not support more than ' +
                             str(cls.MAX_STRING_VALUES) + ' string values')

        # Append counter of string values
        payload_format += 'I'
        payload.append(current_items)

        for string_value in string_values:
            string_value = string_value.encode('ascii')
            len_value = len(string_value)
            payload_format += 'I%ds' % len_value
            payload.extend([len_value, string_value])

        # Build numerical values
        current_items = len(float_values)

        # Append counter of float values
        payload_format += 'I'
        payload.append(current_items)

        if current_items > cls.MAX_FLOAT_VALUES:
            raise ValueError('Protocol does not support more than ' +
                             cls.MAX_FLOAT_VALUES + ' float values')

        payload_format += '%df' % len(float_values)
        payload.extend(float_values)

        packed_payload = struct.pack(cls.BYTE_ORDER + payload_format, *payload)

        message_length = len(packed_payload) + cls.FIXED_HEADER_LEN
        header = [message_length, cls.VERSION, sec, nsec]

        packed_header = struct.pack(
            cls.BYTE_ORDER + cls.HEADER_FORMAT, *header)

        return packed_header + packed_payload

    @classmethod
    def get_message_length(cls, header):
        message_length, _, _, _ = struct.unpack(cls.BYTE_ORDER + cls.HEADER_FORMAT, header)
        return message_length

    @classmethod
    def get_response_key(cls, message):
        """Response key of a message matches the key of a request message,
        i.e. it contains the sequence ID of the message that originated the response."""
        return 'msg:{}'.format(message.feedback_id)


class RobotHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self, request, client_address, server, queue=None):
        self.queue = queue
        super(RobotHandler, self).__init__(request, client_address, server)

    def handle(self):
        last_sequence_id = 0

        while True:
            try:

                current_header = self.request.recv(WireProtocol.FIXED_HEADER_LEN)
                if not current_header:
                    print('Connection broken')
                    return

                wire_message = self.request.recv(1024)
                if not wire_message:
                    print('Connection broken')
                    return

                message = WireProtocol.deserialize(current_header, wire_message)

                if message['sequence_id'] != last_sequence_id + 1:
                    print('Sequence mismatch: current={}, expected={}'.format(
                        message['sequence_id'],
                        last_sequence_id + 1
                    ))

                last_sequence_id = message['sequence_id']

                if not VERBOSE:
                    if message['sequence_id'] % 100 == 0:
                        print('Current sequence id: {}'.format(message['sequence_id']))
                else:
                    print ("{} sent header, Message length={}, sequence_id={}".format(
                            self.client_address[0],
                            WireProtocol.get_message_length(current_header),
                            message['sequence_id'],
                            ))

                if message['feedback_level'] > 0:
                    reply = copy(message)
                    self.queue.put(reply)

            except Exception as e:
                print('[ERROR] {}'.format(str(e)))


def start_receiver(port, q):
    HOST, PORT = '0.0.0.0', port
    print('[RECEIVER] Opening server on port {}'.format(PORT))
    with socketserver.TCPServer((HOST, PORT), partial(RobotHandler, queue=q)) as server:
        print('[RECEIVER] Serving...')
        server.serve_forever()

    print('[RECEIVER] Done')

def start_sender(port, q):
    HOST, PORT = '0.0.0.0', port
    print('[SENDER] Opening server on port {}'.format(PORT))
    with socketserver.TCPServer((HOST, PORT), RobotHandler) as server:
        while True:
            print('[SENDER] Serving...')
            # server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            conn, _addr = server.get_request()
            print('[SENDER] Connection established...')

            while True:
                inst = q.get()
                print('Received message to echo: ' + str(inst))
                conn.sendall(WireProtocol.serialize((inst)))

            print('Connection lost? Will retry...')

    print('[SENDER] Done')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Start echo server to simulate robot(s)')
    parser.add_argument('-n', '--number', type=int, help='Number of robots to simulate', default=1)
    args = parser.parse_args()

    q = queue.Queue()

    RECEIVER_PORT_BASE = 30101
    SENDER_PORT_BASE = 30201

    for i in range(args.number):
        threading.Thread(target=start_receiver, args=(RECEIVER_PORT_BASE + i, q), daemon=True).start()
        threading.Thread(target=start_sender, args=(SENDER_PORT_BASE + i, q), daemon=True).start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Interruped')

    print('Done')
