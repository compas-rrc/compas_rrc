.. currentmodule:: compas_rrc

Custom instructions
-------------------

This library allows to use any RAPID procedure available in the robot controller.
To do that, first create the RAPID procedure in the ``CONTROLLER`` or ``ROBOT`` task,
then invoke it using :class:`CustomInstruction` specifying instruction
name and appropriate parameters. If the procedure generates feedback, it will be
made available as the return value of the call.

The following example calls a procedure named ``r_X000_GoStartPos``::

    # Custom instruction move to start position
    abb.send(rrc.CustomInstruction('r_X000_GoStartPos'))

The RAPID procedure could look like this::

    !************************************************
    ! Function    :     Go to start position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_X000_GoStartPos()
        !
        ! Move to start position
        MoveAbsJ jp_X000_StartPos,v1000,z50,t_A042_Act\WObj:=ob_A042_Act;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Instruction done
            r_A042_FDone;
            !
            ! Check additional feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Cenerate feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                DEFAULT:
                    !
                    ! Not defined
                    !
                    ! Feedback not supported
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC


.. autosummary::
    :toctree: generated/
    :nosignatures:

    CustomInstruction
