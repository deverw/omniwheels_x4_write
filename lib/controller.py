import fischertechnik.factories as txt_factory

txt_factory.init()
txt_factory.init_motor_factory()
txt_factory.init_servomotor_factory()
txt_factory.init_counter_factory()

TXT_M = txt_factory.controller_factory.create_graphical_controller()
TXT_M_M1_encodermotor = txt_factory.motor_factory.create_encodermotor(TXT_M, 1)
TXT_M_M2_encodermotor = txt_factory.motor_factory.create_encodermotor(TXT_M, 2)
TXT_M_M3_encodermotor = txt_factory.motor_factory.create_encodermotor(TXT_M, 3)
TXT_M_M4_encodermotor = txt_factory.motor_factory.create_encodermotor(TXT_M, 4)
TXT_M_S1_servomotor = txt_factory.servomotor_factory.create_servomotor(TXT_M, 1)
TXT_M_C1_motor_step_counter = txt_factory.counter_factory.create_encodermotor_counter(TXT_M, 1)
TXT_M_C1_motor_step_counter.set_motor(TXT_M_M1_encodermotor)
TXT_M_C2_motor_step_counter = txt_factory.counter_factory.create_encodermotor_counter(TXT_M, 2)
TXT_M_C2_motor_step_counter.set_motor(TXT_M_M2_encodermotor)
TXT_M_C3_motor_step_counter = txt_factory.counter_factory.create_encodermotor_counter(TXT_M, 3)
TXT_M_C3_motor_step_counter.set_motor(TXT_M_M3_encodermotor)
TXT_M_C4_motor_step_counter = txt_factory.counter_factory.create_encodermotor_counter(TXT_M, 4)
TXT_M_C4_motor_step_counter.set_motor(TXT_M_M4_encodermotor)

txt_factory.initialized()