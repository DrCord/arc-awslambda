// Read Synchrously
var fs = require("fs");
console.log("\n *START* \n");

var metrics = {
	"vehicle_charging_j1772_plug_inserted": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"woke_status": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"vehicle_started": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"brake_pressed": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"vehicle_direction_state": {
		"type": "int",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"night_mode": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"physical_key_position": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"blinker_timing_flag": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"parking_brake": {
		"type": "int",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 1,
				"num_bits": 2
			}
		]
	},
	"enable_coolant_pump": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"enable_radiator_fan": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"blinker_enable": {
		"type": "int",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 5,
				"num_bits": 2
			}
		]
	},
	"regen_lever_engaged": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"brake_fault": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"park_brake_engaged": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"lv_fault": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"hv_fault": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"seat_belt_not_secured": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"drivetrain_overtemp": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 5,
				"num_bits": 1
			}
		]
	},
	"high_beam_on": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"heater_enable": {
		"type": "bool",
		"address": 257,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 2
			}
		]
	},
	"soc": {
		"type": "float",
		"scale": 2,
		"address": 1024,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"speed": {
		"type": "float",
		"scale": 10,
		"address": 268,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"steering_angle": {
		"type": "int",
		"address": 268,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"odometer": {
		"type": "float",
		"scale": 100,
		"address": 268,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 7,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"controller_1_motor_temperature": {
		"type": "int",
		"address": 267,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"controller_2_motor_temperature": {
		"type": "int",
		"address": 267,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"controller_1_inverter_temperature": {
		"type": "int",
		"address": 267,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"controller_2_inverter_temperature": {
		"type": "int",
		"address": 267,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"controller_1_fault_level": {
		"type": "int",
		"address": 267,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"controller_1_fault_code": {
		"type": "int",
		"address": 267,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"controller_2_fault_level": {
		"type": "int",
		"address": 267,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"controller_2_fault_code": {
		"type": "int",
		"address": 267,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"epsu_current": {
		"type": "float",
        "scale": 1048576,
        "offset": 0,
		"address": 266,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"epsu_unit_temperature": {
		"type": "float",
        "scale": 1,
        "offset": -40,
		"address": 266,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"epsu_encoder_temperature": {
		"type": "float",
        "scale": 1,
        "offset": -40,
		"address": 266,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"fio_park_brake": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"fio_seat_heat_front": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 2,
				"num_bits": 2
			}
		]
	},
	"fio_user_brightness": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"fio_coolant_level_switch_status": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"fio_grip_heat_left": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 2
			}
		]
	},
	"fio_grip_heat_right": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 2,
				"num_bits": 2
			}
		]
	},
	"fio_heater_fan": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"fio_usb_charger": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 6,
				"num_bits": 2
			}
		]
	},
	"fio_stereo": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 2
			}
		]
	},
	"fio_front_acc": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 2,
				"num_bits": 2
			}
		]
	},
	"fio_int_light": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"fio_horn": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 6,
				"num_bits": 2
			}
		]
	},
	"fio_lo_beam_left": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 2
			}
		]
	},
	"fio_hi_beam_left": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 2,
				"num_bits": 2
			}
		]
	},
	"fio_blinker_left": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"fio_fender_light_left": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"fio_left_turn_brightness": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"fio_lo_beam_right": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 2
			}
		]
	},
	"fio_hi_beam_right": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 2,
				"num_bits": 2
			}
		]
	},
	"fio_blinker_right": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"fio_fender_light_right": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"fio_right_turn_brightness": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"fio_coolant_pump": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 2
			}
		]
	},
	"fio_radiator_fan": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 2,
				"num_bits": 2
			}
		]
	},
	"fio_heater_state_request": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"fio_grip_fault_left": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"fio_grip_fault_right": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"fio_wiper": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 4
			}
		]
	},
	"fio_washer_pump": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"fio_right_turn_signal_sw_status": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"fio_left_turn_signal_sw_status": {
		"type": "int",
		"address": 272,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"rio_tail_light_left": {
		"type": "int",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 2
			}
		]
	},
	"rio_tail_light_left_brightness": {
		"type": "int",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"rio_blinker_left_error": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"rio_tail_light_right": {
		"type": "int",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"rio_tail_light_right_brightness": {
		"type": "int",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"rio_blinker_right_error": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"rio_chmsl": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 2
			}
		]
	},
	"rio_reverse_light": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 2,
				"num_bits": 2
			}
		]
	},
	"rio_license_light": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"rio_front_seat_fault": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"rio_rear_seat_fault": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"rio_seat_heat_front": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 2
			}
		]
	},
	"rio_seat_heat_rear": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 2,
				"num_bits": 2
			}
		]
	},
	"rio_seatbelt": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 4,
				"num_bits": 2
			}
		]
	},
	"rio_park_brake_limit": {
		"type": "bool",
		"address": 288,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 6,
				"num_bits": 2
			}
		]
	},
	"hbridge_startup_bit": {
		"type": "int",
		"address": 304,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"hbridge_status": {
		"type": "int",
		"address": 304,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 2,
				"num_bits": 2
			}
		]
	},
	"hbridge_motor_current": {
		"type": "float",
		"scale": 50,
		"address": 304,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_status": {
		"type": "int",
		"address": 773,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_mains_current": {
		"type": "int",
		"address": 773,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_dc_current": {
		"type": "int",
		"address": 773,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_dc_voltage": {
		"type": "int",
		"address": 773,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_mains_frequency": {
		"type": "int",
		"address": 773,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_primary_temperature": {
		"type": "int",
		"address": 774,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_secondary_temperature": {
		"type": "int",
		"address": 774,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_mains_voltage": {
		"type": "int",
		"address": 774,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_max_power": {
		"type": "int",
		"address": 774,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_available_power": {
		"type": "int",
		"address": 774,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_pfc_bus_voltage": {
		"type": "int",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_d2d_primary_heatsink_temperature": {
		"type": "int",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_low_voltage_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 5,
				"num_bits": 1
			}
		]
	},
	"charger_output_no_load_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"charger_pri_to_sec_communication_failure": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"charger_output_short_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"charger_batter_low_voltage_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"charger_can_comm_timeout": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"charger_hardware_failure": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"charger_output_overcurrent_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"charger_output_overvoltage_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 5,
				"num_bits": 1
			}
		]
	},
	"charger_case_over_temperature_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"charger_secd2d_over_temperature_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"charger_sec_topri_communication_fail": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"charger_prid2d_over_temperature_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"charger_pfc_over_temperature_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"charger_bus_under_voltage_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"charger_bus_over_voltage_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 5,
				"num_bits": 1
			}
		]
	},
	"charger_ac_under_voltage_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"charger_ac_over_voltage_protection": {
		"type": "bool",
		"address": 782,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"charger_output_voltage_before_relay": {
		"type": "int",
		"address": 783,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_dc_voltage_set": {
		"type": "int",
		"address": 783,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_dc_current_set": {
		"type": "int",
		"address": 783,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_power_limit": {
		"type": "int",
		"address": 783,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_internal_flag": {
		"type": "int",
		"address": 783,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"charger_factory_test": {
		"type": "int",
		"address": 783,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_pack_soc": {
		"type": "float",
		"scale": 2,
		"address": 1024,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_pack_current": {
		"type": "int",
		"address": 1024,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_pack_instantaneous_voltage": {
		"type": "int",
		"address": 1024,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_relay_state": {
		"type": "int",
		"address": 1024,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_internal_temperature": {
		"type": "int",
		"address": 1024,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_pack_health": {
		"type": "int",
		"address": 1024,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_charge_interlock": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"bms_current_failsafe": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"bms_input_power_supply_failsafe": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"bms_j1772_charge_allowed": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"bms_multi_purpose_enable": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"bms_multi_purpose_input_2": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 5,
				"num_bits": 1
			}
		]
	},
	"bms_multi_purpose_input_3_traction_aux": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"bms_multi_purpose_output": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"bms_multi_purpose_output_2": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"bms_multi_purpose_output_3": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"bms_multi_purpose_output_4": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"bms_relay_failsafe": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"bms_voltage_failsafe": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"bms_ready_power_signal": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"bms_charge_power_signal": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"bms_discharge_relay": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"bms_charge_relay": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"bms_balancing_active": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"bms_error_mil_output": {
		"type": "bool",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 5,
				"num_bits": 1
			}
		]
	},
	"bms_total_pack_cycles": {
		"type": "int",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_failsafe_statuses": {
		"type": "int",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_pack_amp_hours": {
		"type": "int",
		"address": 1025,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 7,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_pack_dcl": {
		"type": "int",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_pack_ccl": {
		"type": "int",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 2,
				"num_bits": 8
			},
			{
				"byte_num": 1,
				"start_bit": 3,
				"num_bits": 8
			}
		]
	},
	"bms_ccl_reduced_high_soc": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"bms_ccl_reduced_high_cell_resistance": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"bms_ccl_reduced_high_cell_v": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"bms_ccl_reduced_high_pack_v": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 5,
				"num_bits": 1
			}
		]
	},
	"bms_ccl_reduced_charger_latch": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"bms_ccl_reduced_alternate_current_lim": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"bms_dcl_reduced_low_soc": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"bms_dcl_reduced_high_cell_resistance": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"bms_dcl_reduced_temperature": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"bms_dcl_reduced_low_cell_v": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"bms_dcl_reduced_low_pack_v": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"bms_dcl_and_ccl_reduced_v_failsafe": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"bms_dcl_and_ccl_reduced_com_failsafe": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a0a_internal_heatsink_thermistor_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a0b_internal_logic_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a0c_highest_cell_voltage_too_high": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a0d_cell_voltage_over_5v_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a0e_lowest_cell_voltage_too_low": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a0f_cell_bank_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 5,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a10_pack_too_hot_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a12_cell_balancing_fault_stuck_off": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a1f_internal_cell_communication_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 0,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a80_weak_cell_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a81_fan_monitor_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0a9c_thermistor_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0aa6_high_voltage_isolation_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0ac0_current_sensor_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 5,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_p0afa_low_cell_voltage_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 6,
				"num_bits": 1
			}
		]
	},
	"bms_dtc_u100_can_communication_fault": {
		"type": "bool",
		"address": 1026,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 7,
				"num_bits": 1
			}
		]
	},

	"bms_low_cell_voltage": {
		"type": "int",
		"address": 1027,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_low_cell_voltage_id": {
		"type": "int",
		"address": 1027,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_high_cell_voltage": {
		"type": "int",
		"address": 1027,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_high_cell_voltage_id": {
		"type": "int",
		"address": 1027,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_j1772_ac_current_limit": {
		"type": "int",
		"address": 1028,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_j1772_ac_power_limit": {
		"type": "int",
		"address": 1028,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_j1772_ac_voltage": {
		"type": "int",
		"address": 1028,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			},
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_j1772_plug_state": {
		"type": "int",
		"address": 1028,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"bms_input_supply_voltage": {
		"type": "int",
		"address": 1028,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"lv_heat1_enable": {
		"type": "bool",
		"address": 1616,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 1,
				"num_bits": 1
			}
		]
	},
	"lv_heat2_enable": {
		"type": "bool",
		"address": 1616,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 2,
				"num_bits": 1
			}
		]
	},
	"lv_dcdc2_enable": {
		"type": "bool",
		"address": 1616,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 3,
				"num_bits": 1
			}
		]
	},
	"lv_sig_beta_key_enable": {
		"type": "bool",
		"address": 1616,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 4,
				"num_bits": 1
			}
		]
	},
	"lv_voltage_1": {
		"type": "int",
		"address": 1617,
		"byte_list": [
			{
				"byte_num": 0,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"lv_voltage_2": {
		"type": "int",
		"address": 1617,
		"byte_list": [
			{
				"byte_num": 1,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"lv_voltage_3": {
		"type": "int",
		"address": 1617,
		"byte_list": [
			{
				"byte_num": 2,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"lv_voltage_4": {
		"type": "int",
		"address": 1617,
		"byte_list": [
			{
				"byte_num": 3,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"lv_current_1": {
		"type": "int",
		"address": 1617,
		"byte_list": [
			{
				"byte_num": 4,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"lv_current_2": {
		"type": "int",
		"address": 1617,
		"byte_list": [
			{
				"byte_num": 5,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"lv_current_3": {
		"type": "int",
		"address": 1617,
		"byte_list": [
			{
				"byte_num": 6,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"lv_current_4": {
		"type": "int",
		"address": 1617,
		"byte_list": [
			{
				"byte_num": 7,
				"start_bit": 0,
				"num_bits": 8
			}
		]
	},
	"humidity": {
		"type": "int"
	 },	 
	 "ambient_temp_c": {
		"type": "float",
		"scale": 10
	 }
}

const telemetry_points = {}
for (const key of Object.keys(metrics)) {
    const title = key.split('_').join(' ')
    const titleCapitalized = toTitleCase(title)
    telemetry_points[key] = {
        "title": titleCapitalized,
        "operator": "mean" ,
		"type": "line_graph",
		"color": "#ffffff"
    }
}

var jsonContent = JSON.stringify(telemetry_points);
console.log(jsonContent);

fs.writeFile("telemetry_points.json", jsonContent, 'utf8', function (err) {
    if (err) {
        console.log("An error occured while writing JSON Object to File.");
        return console.log(err);
    }
 
    console.log("JSON file has been saved.");
});

// console.log("Output Keys : \n", telemetry_points);
console.log("\n *EXIT* \n");

function toTitleCase(str) {
    return str.replace(
        /\w\S*/g,
        function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}