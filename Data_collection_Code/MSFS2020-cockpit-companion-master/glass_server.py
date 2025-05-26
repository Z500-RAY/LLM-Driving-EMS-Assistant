#导入相应库实现功能
from flask import Flask, jsonify, render_template, request
from SimConnect import *
from time import sleep
import random

#构建Flask应用
app = Flask(__name__)

# SIMCONNECTION RELATED STARTUPS

# SimConnect初始化和请求定义
sm = SimConnect()
ae = AircraftEvents(sm)
#关注一下_time参数的含义
aq = AircraftRequests(sm, _time=10)

# Create request holders

# Note: I have commented out request_ui as I don't think it makes sense to replicate the ui interface through JSON given the /ui endpoint returns a duplicate of this anyway
# I have not deleted it yet as it's handy to have this list of helpful variables here
#
#request_ui = [
#	'PLANE_ALTITUDE', #飞机高度
#	'PLANE_LATITUDE', #飞机纬度
#	'PLANE_LONGITUDE', #飞机经度
#	'AIRSPEED_INDICATED', #指示空速
#	'MAGNETIC_COMPASS',  # 磁罗盘读数
#	'VERTICAL_SPEED',  # 垂直速度指示
#	'FLAPS_HANDLE_PERCENT',  # 襟翼手柄扩展百分比
#	'FUEL_TOTAL_QUANTITY',  # 当前燃油量（单位体积）
#	'FUEL_TOTAL_CAPACITY',  # 飞机总燃油容量
#	'GEAR_HANDLE_POSITION',  # 起落架手柄位置（应用时为True）
#	'AUTOPILOT_MASTER', #自动驾驶主开关
#	'AUTOPILOT_NAV_SELECTED',
#	'AUTOPILOT_WING_LEVELER',
#	'AUTOPILOT_HEADING_LOCK',
#	'AUTOPILOT_HEADING_LOCK_DIR',
#	'AUTOPILOT_ALTITUDE_LOCK',
#	'AUTOPILOT_ALTITUDE_LOCK_VAR',
#	'AUTOPILOT_ATTITUDE_HOLD',
#	'AUTOPILOT_GLIDESLOPE_HOLD',
#	'AUTOPILOT_PITCH_HOLD_REF',
#	'AUTOPILOT_APPROACH_HOLD',
#	'AUTOPILOT_BACKCOURSE_HOLD',
#	'AUTOPILOT_VERTICAL_HOLD',
#	'AUTOPILOT_VERTICAL_HOLD_VAR',
#	'AUTOPILOT_PITCH_HOLD',
#	'AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE',
#	'AUTOPILOT_AIRSPEED_HOLD',
#	'AUTOPILOT_AIRSPEED_HOLD_VAR'
#]

#定义数据请求列表
request_location = [
	'PLANE_ALTITUDE',
	'GROUND_ALTITUDE',
	'PLANE_LATITUDE',
	'PLANE_LONGITUDE',
	'KOHLSMAN',
]

request_airspeed = [
	'AIRSPEED_TRUE',
	'AIRSPEED_INDICATED',
	'AIRSPEED_TRUE CALIBRATE',
	'AIRSPEED_BARBER POLE',
	'AIRSPEED_MACH',
]

request_compass = [
	'WISKEY_COMPASS_INDICATION_DEGREES',
	'PARTIAL_PANEL_COMPASS',
	'ADF_CARD',  # ADF compass rose setting
	'MAGNETIC_COMPASS',  # Compass reading                     
	'INDUCTOR_COMPASS_PERCENT_DEVIATION',  # Inductor compass deviation reading
	'INDUCTOR_COMPASS_HEADING_REF',  # Inductor compass heading
]

request_vertical_speed = [
	'VELOCITY_BODY_Y',  # True vertical speed, relative to aircraft axis
	'RELATIVE_WIND_VELOCITY_BODY_Y',  # Vertical speed relative to wind
	'VERTICAL_SPEED',  # Vertical speed indication
	'GPS_WP_VERTICAL_SPEED',  # Vertical speed to waypoint
]

request_fuel = [
	'FUEL_TANK_CENTER_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_CENTER2_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_CENTER3_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_LEFT_MAIN_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_LEFT_AUX_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_LEFT_TIP_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_RIGHT_MAIN_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_RIGHT_AUX_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_RIGHT_TIP_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_EXTERNAL1_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_EXTERNAL2_LEVEL',  # Percent of maximum capacity
	'FUEL_TANK_CENTER_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_CENTER2_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_CENTER3_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_LEFT_MAIN_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_LEFT_AUX_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_LEFT_TIP_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_RIGHT_MAIN_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_RIGHT_AUX_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_RIGHT_TIP_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_EXTERNAL1_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_EXTERNAL2_CAPACITY',  # Maximum capacity in volume
	'FUEL_LEFT_CAPACITY',  # Maximum capacity in volume
	'FUEL_RIGHT_CAPACITY',  # Maximum capacity in volume
	'FUEL_TANK_CENTER_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_CENTER2_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_CENTER3_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_LEFT_MAIN_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_LEFT_AUX_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_LEFT_TIP_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_RIGHT_MAIN_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_RIGHT_AUX_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_RIGHT_TIP_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_EXTERNAL1_QUANTITY',  # Current quantity in volume
	'FUEL_TANK_EXTERNAL2_QUANTITY',  # Current quantity in volume
	'FUEL_LEFT_QUANTITY',  # Current quantity in volume
	'FUEL_RIGHT_QUANTITY',  # Current quantity in volume
	'FUEL_TOTAL_QUANTITY',  # Current quantity in volume
	'FUEL_WEIGHT_PER_GALLON',  # Fuel weight per gallon
	'FUEL_TOTAL_CAPACITY',  # Total capacity of the aircraft
	'FUEL_SELECTED_QUANTITY_PERCENT',  # Percent or capacity for selected tank
	'FUEL_SELECTED_QUANTITY',  # Quantity of selected tank
	'FUEL_TOTAL_QUANTITY_WEIGHT',  # Current total fuel weight of the aircraft
	'NUM_FUEL_SELECTORS',  # Number of selectors on the aircraft
	'UNLIMITED_FUEL',  # Unlimited fuel flag
	'ESTIMATED_FUEL_FLOW',  # Estimated fuel flow at cruise
]

request_flaps = [
	'FLAPS_HANDLE_PERCENT',  # 襟翼手柄的百分比扩展程度。表示襟翼手柄相对于其最大扩展位置的百分比
	'FLAPS_HANDLE_INDEX',  # 当前襟翼手柄位置的索引。表示手柄所处的预设位置的整数值
	'FLAPS_NUM_HANDLE_POSITIONS',  # 襟翼手柄的预设位置数量。表示襟翼手柄可以设置的不同位置的数量
	'TRAILING_EDGE_FLAPS_LEFT_PERCENT',  # 左侧后缘襟翼的百分比扩展程度。表示左侧后缘襟翼相对于其最大扩展位置的百分比
	'TRAILING_EDGE_FLAPS_RIGHT_PERCENT',  # 右侧后缘襟翼的百分比扩展程度。表示右侧后缘襟翼相对于其最大扩展位置的百分比
	'TRAILING_EDGE_FLAPS_LEFT_ANGLE',  # Angle left trailing edge flap extended. Use TRAILING EDGE FLAPS LEFT PERCENT to set a value.
	'TRAILING_EDGE_FLAPS_RIGHT_ANGLE',  # Angle right trailing edge flap extended. Use TRAILING EDGE FLAPS RIGHT PERCENT to set a value.
	'LEADING_EDGE_FLAPS_LEFT_PERCENT',  # Percent left leading edge flap extended
	'LEADING_EDGE_FLAPS_RIGHT_PERCENT',  # Percent right leading edge flap extended
	'LEADING_EDGE_FLAPS_LEFT_ANGLE',  # Angle left leading edge flap extended. Use LEADING EDGE FLAPS LEFT PERCENT to set a value.
	'LEADING_EDGE_FLAPS_RIGHT_ANGLE',  # Angle right leading edge flap extended. Use LEADING EDGE FLAPS RIGHT PERCENT to set a value.
	'FLAPS_AVAILABLE',  # 如果襟翼可用，则为 True
	'FLAP_DAMAGE_BY_SPEED',  # 如果襟翼因过高的速度而受损，则为 True
	'FLAP_SPEED_EXCEEDED',  #  如果超过了襟翼的安全速度限制，则为 True
]

request_throttle = [
	'AUTOPILOT_THROTTLE_ARM',  # 自动油门启用状态
	'AUTOPILOT_TAKEOFF_POWER_ACTIVE',  # 起飞/复飞动力模式启用
	'AUTOTHROTTLE_ACTIVE',  # 自动油门激活状态
	'FULL_THROTTLE_THRUST_TO_WEIGHT_RATIO',  # 全油门推重比
	'THROTTLE_LOWER_LIMIT', # 油门下限
	# 'GENERAL_ENG_THROTTLE_LEVER_POSITION:index',  # 发动机油门杆位置，百分比形式
	'GENERAL_ENG_THROTTLE_LEVER_POSITION:1',  # 发动机油门杆位置，百分比形式
	'AUTOPILOT_THROTTLE_ARM',  # Autothrottle armed
	'AUTOTHROTTLE_ACTIVE',  # Auto-throttle active
	'FULL_THROTTLE_THRUST_TO_WEIGHT_RATIO',  # Full throttle thrust to weight ratio
]

request_gear = [
	'IS_GEAR_RETRACTABLE',  # True if gear can be retracted
	'IS_GEAR_SKIS',  # True if landing gear is skis
	'IS_GEAR_FLOATS',  # True if landing gear is floats
	'IS_GEAR_SKIDS',  # True if landing gear is skids
	'IS_GEAR_WHEELS',  # True if landing gear is wheels
	'GEAR_HANDLE_POSITION',  # True if gear handle is applied
	'GEAR_HYDRAULIC_PRESSURE',  # Gear hydraulic pressure
	'TAILWHEEL_LOCK_ON',  # True if tailwheel lock applied
	'GEAR_CENTER_POSITION',  # Percent center gear extended
	'GEAR_LEFT_POSITION',  # Percent left gear extended
	'GEAR_RIGHT_POSITION',  # Percent right gear extended
	'GEAR_TAIL_POSITION',  # Percent tail gear extended
	'GEAR_AUX_POSITION',  # Percent auxiliary gear extended
	'GEAR_TOTAL_PCT_EXTENDED',  # Percent total gear extended
	'AUTO_BRAKE_SWITCH_CB',  # Auto brake switch position
	'WATER_RUDDER_HANDLE_POSITION',
	'WATER_LEFT_RUDDER_EXTENDED',  # Percent extended
	'WATER_RIGHT_RUDDER_EXTENDED',  # Percent extended
	'GEAR_CENTER_STEER_ANGLE',  # Center wheel angle, negative to the left, positive to the right.
	'GEAR_LEFT_STEER_ANGLE',  # Left wheel angle, negative to the left, positive to the right.
	'GEAR_RIGHT_STEER_ANGLE',  # Right wheel angle, negative to the left, positive to the right.
	'GEAR_AUX_STEER_ANGLE',  # Aux wheel angle, negative to the left, positive to the right. The aux wheel is the fourth set of gear, sometimes used on helicopters.
	'WATER_LEFT_RUDDER_STEER_ANGLE',  # Water left rudder angle, negative to the left, positive to the right.
	'WATER_RIGHT_RUDDER_STEER_ANGLE',  # Water right rudder angle, negative to the left, positive to the right.
	'GEAR_CENTER_STEER_ANGLE_PCT',  # Center steer angle as a percentage
	'GEAR_LEFT_STEER_ANGLE_PCT',  # Left steer angle as a percentage
	'GEAR_RIGHT_STEER_ANGLE_PCT',  # Right steer angle as a percentage
	'GEAR_AUX_STEER_ANGLE_PCT',  # Aux steer angle as a percentage
	'WATER_LEFT_RUDDER_STEER_ANGLE_PCT',  # Water left rudder angle as a percentage
	'WATER_RIGHT_RUDDER_STEER_ANGLE_PCT',  # Water right rudder as a percentage
	'CENTER_WHEEL_RPM',  # Center landing gear rpm
	'LEFT_WHEEL_RPM',  # Left landing gear rpm
	'RIGHT_WHEEL_RPM',  # Right landing gear rpm
	'AUX_WHEEL_RPM',  # Rpm of fourth set of gear wheels.
	'CENTER_WHEEL_ROTATION_ANGLE',  # Center wheel rotation angle
	'LEFT_WHEEL_ROTATION_ANGLE',  # Left wheel rotation angle
	'RIGHT_WHEEL_ROTATION_ANGLE',  # Right wheel rotation angle
	'AUX_WHEEL_ROTATION_ANGLE',  # Aux wheel rotation angle
	'GEAR_EMERGENCY_HANDLE_POSITION',  # True if gear emergency handle applied
	'ANTISKID_BRAKES_ACTIVE',  # True if antiskid brakes active
	'RETRACT_FLOAT_SWITCH',  # True if retract float switch on
	'RETRACT_LEFT_FLOAT_EXTENDED',  # If aircraft has retractable floats.
	'RETRACT_RIGHT_FLOAT_EXTENDED',  # If aircraft has retractable floats.
	'STEER_INPUT_CONTROL',  # Position of steering tiller
	'GEAR_DAMAGE_BY_SPEED',  # True if gear has been damaged by excessive speed
	'GEAR_SPEED_EXCEEDED',  # True if safe speed limit for gear exceeded
	'NOSEWHEEL_LOCK_ON',  # True if the nosewheel lock is engaged.
]

request_trim = [
	'ROTOR_LATERAL_TRIM_PCT',  # 旋翼的横向修整百分比。用于直升机等具有旋翼的飞机，显示旋翼的修整状态
	'ELEVATOR_TRIM_POSITION',  # 升降舵的修整位置，表示升降舵的偏转位置。通常以角度度数表示，显示飞机在纵向上的调整
	'ELEVATOR_TRIM_INDICATOR', # 升降舵修整指示器。通常用于显示升降舵的修整状态，可能以指示器或刻度显示
	'ELEVATOR_TRIM_PCT',  # 升降舵的修整百分比，表示升降舵的修整程度，0% 代表没有修整，100% 代表最大修整
	'AILERON_TRIM',  # 副翼的修整角度，表示副翼的实际偏转角度。通常以角度度数表示
	'AILERON_TRIM_PCT',  #  副翼的修整百分比，表示副翼的修整程度，0% 代表没有修整，100% 代表最大修整
	'RUDDER_TRIM_PCT',  # 方向舵的修整百分比，表示方向舵的修整程度。0% 代表没有修整，100% 代表最大修整
	'RUDDER_TRIM',  # 方向舵的修整角度，表示方向舵的实际偏转角度。通常以角度度数表示
]

request_autopilot = [
	'AUTOPILOT_MASTER',
	'AUTOPILOT_AVAILABLE',
	'AUTOPILOT_NAV_SELECTED',
	'AUTOPILOT_WING_LEVELER',
	'AUTOPILOT_NAV1_LOCK',
	'AUTOPILOT_HEADING_LOCK',
	'AUTOPILOT_HEADING_LOCK_DIR',
	'AUTOPILOT_ALTITUDE_LOCK',
	'AUTOPILOT_ALTITUDE_LOCK_VAR',
	'AUTOPILOT_ATTITUDE_HOLD',
	'AUTOPILOT_GLIDESLOPE_HOLD',
	'AUTOPILOT_PITCH_HOLD_REF',
	'AUTOPILOT_APPROACH_HOLD',
	'AUTOPILOT_BACKCOURSE_HOLD',
	'AUTOPILOT_VERTICAL_HOLD_VAR',
	'AUTOPILOT_PITCH_HOLD',
	'AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE',
	'AUTOPILOT_FLIGHT_DIRECTOR_PITCH',
	'AUTOPILOT_FLIGHT_DIRECTOR_BANK',
	'AUTOPILOT_AIRSPEED_HOLD',
	'AUTOPILOT_AIRSPEED_HOLD_VAR',
	'AUTOPILOT_MACH_HOLD',
	'AUTOPILOT_MACH_HOLD_VAR',
	'AUTOPILOT_YAW_DAMPER',
	'AUTOPILOT_RPM_HOLD_VAR',
	'AUTOPILOT_THROTTLE_ARM',
	'AUTOPILOT_TAKEOFF_POWER ACTIVE',
	'AUTOTHROTTLE_ACTIVE',
	'AUTOPILOT_VERTICAL_HOLD',
	'AUTOPILOT_RPM_HOLD',
	'AUTOPILOT_MAX_BANK',
	'FLY_BY_WIRE_ELAC_SWITCH',
	'FLY_BY_WIRE_FAC_SWITCH',
	'FLY_BY_WIRE_SEC_SWITCH',
	'FLY_BY_WIRE_ELAC_FAILED',
	'FLY_BY_WIRE_FAC_FAILED',
	'FLY_BY_WIRE_SEC_FAILED'
]

request_cabin = [
	'CABIN_SEATBELTS_ALERT_SWITCH',
	'CABIN_NO_SMOKING_ALERT_SWITCH'
]

request_pitch = [
	'PLANE_PITCH_DEGREES',
	'ATTITUDE_INDICATOR_PITCH_DEGREES'
]

request_detect = [
	#飞行高度Altitude:包括相对于海平面的高度（MSL）和相对于地面的高度（AGL）。大坡度盘旋时，通常会有高度的变化。
	'PLANE_ALTITUDE',#单位是feets
	'GROUND_ALTITUDE',#单位是meters
	#飞机俯仰角Pitch Angle:表示飞机的机头相对于地平线的角度。
	'PLANE_PITCH_DEGREES', #单位是radians
	#飞机滚转角Roll Angle:表示飞机相对于地平线的倾斜角度。大坡度盘旋通常伴随着较大的滚转角。
	'PLANE_BANK_DEGREES', #单位是radians
	#偏航角Yaw Angle:表示飞机的机头方向相对于地面的角度。
	#航向Heading:当前飞机的航向。
	'PLANE_HEADING_DEGREES_TRUE', #单位是radians
	'PLANE_HEADING_DEGREES_MAGNETIC', #单位是radians
	#空速Airspeed:包括指示空速（IAS）、真空速（TAS）等。在盘旋过程中，空速可能会变化。
	'AIRSPEED_INDICATED', #指示空速（Indicated Airspeed, IAS），这是从空速表直接读出的速度，未校正误差。单位是knots
	'AIRSPEED_TRUE', #真空速（True Airspeed, TAS），这是飞机相对于周围空气的真实速度。单位是knots
	'GROUND_VELOCITY', #地速（Ground Speed），这是飞机相对于地面的速度，单位是knots
	#垂直速度Vertical Speed:表示飞机的爬升或下降速度。
	'VERTICAL_SPEED',#单位是feet per second
	#侧滑角Sideslip Angle，偏航率Yaw Rate:这些数据能够帮助判断飞机是否处于协调转弯中。
	'INCIDENCE_BETA',#单位是radians
	#加速度Acceleration:包括纵向、横向和垂直方向的加速度数据。可以用于检测重力变化和其他动态情况。
	'ACCELERATION_BODY_X', #表示沿飞机纵轴（前后方向）的加速度，单位是feet per second squared
	'ACCELERATION_BODY_Y', #表示沿飞机横轴（左右方向）的加速度，单位是feet per second squared
	'ACCELERATION_BODY_Z', #表示沿飞机竖轴（上下方向）的加速度，单位是feet per second squared
	#攻角Angle of Attack, AOA:表示机翼迎角，特别是在大坡度盘旋时，这个数据非常关键。
	'INCIDENCE_ALPHA', #	单位是radians
]

def thousandify(x):
	return f"{x:,}"


@app.route('/')
def glass():
	return render_template("glass.html")


@app.route('/attitude-indicator')
def AttInd():
	return render_template("attitude-indicator/index.html")


def get_dataset(data_type):
	if data_type == "navigation": request_to_action = request_location
	if data_type == "airspeed": request_to_action = request_airspeed
	if data_type == "compass": request_to_action = request_compass
	if data_type == "vertical_speed": request_to_action = request_vertical_speed
	if data_type == "fuel": request_to_action = request_fuel
	if data_type == "flaps": request_to_action = request_flaps
	if data_type == "throttle": request_to_action = request_throttle
	if data_type == "gear": request_to_action = request_gear
	if data_type == "trim": request_to_action = request_trim
	if data_type == "autopilot": request_to_action = request_autopilot
	if data_type == 'cabin': request_to_action = request_cabin
	if data_type == 'pitch': request_to_action = request_pitch
	if data_type == 'detect': request_to_action = request_detect
	#if data_type == "ui": request_to_action = request_ui   # see comment above as to why I've removed this

	return request_to_action


#获取ui变量的JSON数据
@app.route('/ui')
def output_ui_variables():

	# Initialise dictionaru
	ui_friendly_dictionary = {}
	ui_friendly_dictionary["STATUS"] = "success"

	# Fuel
	fuel_percentage = (aq.get("FUEL_TOTAL_QUANTITY") / aq.get("FUEL_TOTAL_CAPACITY")) * 100
	ui_friendly_dictionary["FUEL_PERCENTAGE"] = round(fuel_percentage)
	ui_friendly_dictionary["AIRSPEED_INDICATE"] = round(aq.get("AIRSPEED_INDICATED"))
	ui_friendly_dictionary["ALTITUDE"] = thousandify(round(aq.get("PLANE_ALTITUDE")))

	# Control surfaces
	if aq.get("GEAR_HANDLE_POSITION") == 1:
		ui_friendly_dictionary["GEAR_HANDLE_POSITION"] = "DOWN"
	else:
		ui_friendly_dictionary["GEAR_HANDLE_POSITION"] = "UP"
	ui_friendly_dictionary["FLAPS_HANDLE_PERCENT"] = round(aq.get("FLAPS_HANDLE_PERCENT") * 100)

	ui_friendly_dictionary["ELEVATOR_TRIM_PCT"] = round(aq.get("ELEVATOR_TRIM_PCT") * 100)
	ui_friendly_dictionary["RUDDER_TRIM_PCT"] = round(aq.get("RUDDER_TRIM_PCT") * 100)

	# Navigation
	ui_friendly_dictionary["LATITUDE"] = aq.get("PLANE_LATITUDE")
	# print(f"LATITUDE: {ui_friendly_dictionary['LATITUDE']}")
	ui_friendly_dictionary["LONGITUDE"] = aq.get("PLANE_LONGITUDE")
	# print(f"LONGITUDE: {ui_friendly_dictionary['LONGITUDE']}")
	ui_friendly_dictionary["MAGNETIC_COMPASS"] = round(aq.get("MAGNETIC_COMPASS"))
	# print(f"MAGNETIC_COMPASS: {ui_friendly_dictionary['MAGNETIC_COMPASS']}")
	ui_friendly_dictionary["VERTICAL_SPEED"] = round(aq.get("VERTICAL_SPEED"))
	# print(f"VERTICAL_SPEED: {ui_friendly_dictionary['VERTICAL_SPEED']}")

	# Autopilot
	ui_friendly_dictionary["AUTOPILOT_MASTER"] = aq.get("AUTOPILOT_MASTER")
	ui_friendly_dictionary["AUTOPILOT_NAV_SELECTED"] = aq.get("AUTOPILOT_NAV_SELECTED")
	ui_friendly_dictionary["AUTOPILOT_WING_LEVELER"] = aq.get("AUTOPILOT_WING_LEVELER")
	ui_friendly_dictionary["AUTOPILOT_HEADING_LOCK"] = aq.get("AUTOPILOT_HEADING_LOCK")
	ui_friendly_dictionary["AUTOPILOT_HEADING_LOCK_DIR"] = round(aq.get("AUTOPILOT_HEADING_LOCK_DIR"))
	ui_friendly_dictionary["AUTOPILOT_ALTITUDE_LOCK"] = aq.get("AUTOPILOT_ALTITUDE_LOCK")
	ui_friendly_dictionary["AUTOPILOT_ALTITUDE_LOCK_VAR"] = thousandify(round(aq.get("AUTOPILOT_ALTITUDE_LOCK_VAR")))
	ui_friendly_dictionary["AUTOPILOT_ATTITUDE_HOLD"] = aq.get("AUTOPILOT_ATTITUDE_HOLD")
	ui_friendly_dictionary["AUTOPILOT_GLIDESLOPE_HOLD"] = aq.get("AUTOPILOT_GLIDESLOPE_HOLD")
	ui_friendly_dictionary["AUTOPILOT_APPROACH_HOLD"] = aq.get("AUTOPILOT_APPROACH_HOLD")
	ui_friendly_dictionary["AUTOPILOT_BACKCOURSE_HOLD"] = aq.get("AUTOPILOT_BACKCOURSE_HOLD")
	ui_friendly_dictionary["AUTOPILOT_VERTICAL_HOLD"] = aq.get("AUTOPILOT_VERTICAL_HOLD")
	ui_friendly_dictionary["AUTOPILOT_VERTICAL_HOLD_VAR"] = aq.get("AUTOPILOT_VERTICAL_HOLD_VAR")
	ui_friendly_dictionary["AUTOPILOT_PITCH_HOLD"] = aq.get("AUTOPILOT_PITCH_HOLD")
	ui_friendly_dictionary["AUTOPILOT_PITCH_HOLD_REF"] = aq.get("AUTOPILOT_PITCH_HOLD_REF")
	ui_friendly_dictionary["AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE"] = aq.get("AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE")
	ui_friendly_dictionary["AUTOPILOT_AIRSPEED_HOLD"] = aq.get("AUTOPILOT_AIRSPEED_HOLD")
	ui_friendly_dictionary["AUTOPILOT_AIRSPEED_HOLD_VAR"] = round(aq.get("AUTOPILOT_AIRSPEED_HOLD_VAR"))

	# Cabin
	ui_friendly_dictionary["CABIN_SEATBELTS_ALERT_SWITCH"] = aq.get("CABIN_SEATBELTS_ALERT_SWITCH")
	ui_friendly_dictionary["CABIN_NO_SMOKING_ALERT_SWITCH"] = aq.get("CABIN_NO_SMOKING_ALERT_SWITCH")

	#detect
	ui_friendly_dictionary["PLANE_ALTITUDE"] = aq.get("PLANE_ALTITUDE")
	ui_friendly_dictionary["GROUND_ALTITUDE"] = aq.get("GROUND_ALTITUDE")
	ui_friendly_dictionary["PLANE_PITCH_DEGREES"] = aq.get("PLANE_PITCH_DEGREES")
	ui_friendly_dictionary["PLANE_BANK_DEGREES"] = aq.get("PLANE_BANK_DEGREES")
	ui_friendly_dictionary["PLANE_HEADING_DEGREES_TRUE"] = aq.get("PLANE_HEADING_DEGREES_TRUE")
	ui_friendly_dictionary["PLANE_HEADING_DEGREES_MAGNETIC"] = aq.get("PLANE_HEADING_DEGREES_MAGNETIC")
	ui_friendly_dictionary["AIRSPEED_INDICATED"] = aq.get("AIRSPEED_INDICATED")
	ui_friendly_dictionary["AIRSPEED_TRUE"] = aq.get("AIRSPEED_TRUE")
	ui_friendly_dictionary["GROUND_VELOCITY"] = aq.get("GROUND_VELOCITY")
	ui_friendly_dictionary["VERTICAL_SPEED"] = aq.get("VERTICAL_SPEED")
	ui_friendly_dictionary["INCIDENCE_BETA"] = aq.get("INCIDENCE_BETA")
	ui_friendly_dictionary["ACCELERATION_BODY_X"] = aq.get("ACCELERATION_BODY_X")
	ui_friendly_dictionary["ACCELERATION_BODY_Y"] = aq.get("ACCELERATION_BODY_Y")
	ui_friendly_dictionary["ACCELERATION_BODY_Z"] = aq.get("ACCELERATION_BODY_Z")
	ui_friendly_dictionary["INCIDENCE_ALPHA"] = aq.get("INCIDENCE_ALPHA")
	return jsonify(ui_friendly_dictionary)

@app.route('/log_data', methods=['POST'])
def log_data():
    # Get the JSON data sent from the client-side
    data = request.get_json()

    # You can print the data to the console
    print("Received simulator data:", data)

    # Optionally, write the data to a file
    with open(r"C:\Users\888\Desktop\simulator_data.txt", "a") as log_file:
        log_file.write(str(data) + "\n")

    return jsonify(success=True), 200

@app.route('/dataset/<dataset_name>/', methods=["GET"])
def output_json_dataset(dataset_name):
	dataset_map = {}  #I have renamed map to dataset_map as map is used elsewhere
	data_dictionary = get_dataset(dataset_name)
	for datapoint_name in data_dictionary:
		dataset_map[datapoint_name] = aq.get(datapoint_name)
	return jsonify(dataset_map)


def get_datapoint(datapoint_name, index=None):
	# This function actually does the work of getting the datapoint

	if index is not None and ':index' in datapoint_name:
		dp = aq.find(datapoint_name)
		if dp is not None:
			dp.setIndex(int(index))

	return aq.get(datapoint_name)


@app.route('/datapoint/<datapoint_name>/get', methods=["GET"])
def get_datapoint_endpoint(datapoint_name):
	# This is the http endpoint wrapper for getting a datapoint

	ds = request.get_json() if request.is_json else request.form
	index = ds.get('index')

	output = get_datapoint(datapoint_name, index)

	if isinstance(output, bytes):
		output = output.decode('ascii')

	return jsonify(output)


def set_datapoint(datapoint_name, index=None, value_to_use=None):
	# This function actually does the work of setting the datapoint

	if index is not None and ':index' in datapoint_name:
		clas = aq.find(datapoint_name)
		if clas is not None:
			clas.setIndex(int(index))

	sent = False
	if value_to_use is None:
		sent = aq.set(datapoint_name, 0)
	else:
		sent = aq.set(datapoint_name, int(value_to_use))

	if sent is True:
		status = "success"
	else:
		status = "Error with sending request: %s" % (datapoint_name)

	return status


@app.route('/datapoint/<datapoint_name>/set', methods=["POST"])
def set_datapoint_endpoint(datapoint_name):
	# This is the http endpoint wrapper for setting a datapoint

	ds = request.get_json() if request.is_json else request.form
	index = ds.get('index')
	value_to_use = ds.get('value_to_use')

	status = set_datapoint (datapoint_name, index, value_to_use)

	return jsonify(status)


def trigger_event(event_name, value_to_use = None):
	# This function actually does the work of triggering the event

	EVENT_TO_TRIGGER = ae.find(event_name)
	if EVENT_TO_TRIGGER is not None:
		if value_to_use is None:
			EVENT_TO_TRIGGER()
		else:
			EVENT_TO_TRIGGER(int(value_to_use))

		status = "success"
	else:
		status = "Error: %s is not an Event" % (event_name)

	return status


@app.route('/event/<event_name>/trigger', methods=["POST"])
def trigger_event_endpoint(event_name):
	# This is the http endpoint wrapper for triggering an event

	ds = request.get_json() if request.is_json else request.form
	value_to_use = ds.get('value_to_use')

	status = trigger_event(event_name, value_to_use)

	return jsonify(status)


@app.route('/custom_emergency/<emergency_type>', methods=["GET", "POST"])
def custom_emergency(emergency_type):

	text_to_return = "No valid emergency type passed"

	if emergency_type == "random_engine_fire":
		# Calculate number of engines
		number_of_engines = aq.get("NUMBER_OF_ENGINES")

		if number_of_engines < 0: return "error, no engines found - is sim running?"
		engine_to_set_on_fire = random.randint(1,number_of_engines)

		set_datapoint("ENG_ON_FIRE:index", engine_to_set_on_fire, 1)

		text_to_return = "Engine " + str(engine_to_set_on_fire) + " on fire"

	return text_to_return


app.run(host='0.0.0.0', port=5000, debug=True)