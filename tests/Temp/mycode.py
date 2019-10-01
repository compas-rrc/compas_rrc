from compas.geometry import Frame
print("")
print("Code Start")
print("******************************************")
print("")


pos = [10, 20, 30]
orient = [0, 1, 0, 0]

test = Frame.from_quaternion(orient,pos)

# version control test

print(test.xaxis)

print("")
print("******************************************")
print("Code End")
print("")
