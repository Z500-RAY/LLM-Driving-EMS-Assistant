let altitude;
let fuel_percentage;
let compass;
let airspeed;
let latitude;
let longitude;

let autopilot_master;
let autopilot_nav_selected;
let autopilot_wing_leveler;
let autopilot_heading_lock;
let autopilot_heading_lock_dir;
let autopilot_altitude_lock;
let autopilot_altitude_lock_var;
let autopilot_attitude_hold;
let autopilot_glidescope_hold;
let autopilot_approach_hold;
let autopilot_backcourse_hold;
let autopilot_vertical_hold;
let autopilot_vertical_hold_var;
let autopilot_pitch_hold;
let autopilot_pitch_hold_ref;
let autopilot_flight_director_active;
let autopilot_airspeed_hold;
let autopilot_airspeed_hold_var;

let gear_handle_position;
let elevator_trim_pct;
let elevator_trim_pct_reversed;
let rudder_trim_pct;
let flaps_handle_pct;
let flaps_handle_pct_reversed;

let cabin_seatbelts_alert_switch;
let cabin_no_smoking_alert_switch;

let plane_altitude;
let ground_altitude;
let plane_pitch_degrees;
let plane_bank_degrees;
let plane_heading_degrees_true;
let plane_heading_degrees_magnetic;
let airspeed_indicated;
let airspeed_true;
let ground_velocity;
let vertical_speed;
let incidence_beta;
let acceleration_body_x;
let acceleration_body_y;
let acceleration_body_z;
let incidence_alpha;


window.setInterval(function(){
    getSimulatorData();
    displayData()
    updateMap()
}, 500);


function getSimulatorData() {
    $.getJSON($SCRIPT_ROOT + '/ui', {}, function(data) {

        //Navigation
        altitude = data.ALTITUDE;
        vertical_speed = data.VERTICAL_SPEED;
        compass = data.MAGNETIC_COMPASS;
        airspeed = data.AIRSPEED_INDICATE;
        latitude = data.LATITUDE;
        longitude = data.LONGITUDE;

        //Fuel
        fuel_percentage = data.FUEL_PERCENTAGE;

        //Autopilot
        autopilot_master = data.AUTOPILOT_MASTER;
        autopilot_nav_selected = data.AUTOPILOT_NAV_SELECTED;
        autopilot_wing_leveler = data.AUTOPILOT_WING_LEVELER;
        autopilot_heading_lock = data.AUTOPILOT_HEADING_LOCK;
        autopilot_heading_lock_dir = data.AUTOPILOT_HEADING_LOCK_DIR;
        autopilot_altitude_lock = data.AUTOPILOT_ALTITUDE_LOCK;
        autopilot_altitude_lock_var = data.AUTOPILOT_ALTITUDE_LOCK_VAR;
        autopilot_attitude_hold = data.AUTOPILOT_ATTITUDE_HOLD;
        autopilot_glidescope_hold = data.AUTOPILOT_GLIDESLOPE_HOLD;
        autopilot_approach_hold = data.AUTOPILOT_APPROACH_HOLD;
        autopilot_backcourse_hold = data.AUTOPILOT_BACKCOURSE_HOLD;
        autopilot_vertical_hold = data.AUTOPILOT_VERTICAL_HOLD
        autopilot_vertical_hold_var = data.AUTOPILOT_VERTICAL_HOLD_VAR;
        autopilot_pitch_hold = data.AUTOPILOT_PITCH_HOLD;
        autopilot_pitch_hold_ref = data.AUTOPILOT_PITCH_HOLD_REF;
        autopilot_flight_director_active = data.AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE;
        autopilot_airspeed_hold = data.AUTOPILOT_AIRSPEED_HOLD;
        autopilot_airspeed_hold_var = data.AUTOPILOT_AIRSPEED_HOLD_VAR;

        //Control surfaces
        gear_handle_position = data.GEAR_HANDLE_POSITION;
        elevator_trim_pct = data.ELEVATOR_TRIM_PCT;
        elevator_trim_pct_reversed = - elevator_trim_pct
        //rudder_trim_pct = data.RUDDER_TRIM_PCT;
        flaps_handle_pct = data.FLAPS_HANDLE_PERCENT;
        flaps_handle_pct_reversed = - flaps_handle_pct;

        //Cabin
        cabin_no_smoking_alert_switch = data.CABIN_NO_SMOKING_ALERT_SWITCH;
        cabin_seatbelts_alert_switch = data.CABIN_SEATBELTS_ALERT_SWITCH;

        //Detect
        plane_altitude=data.PLANE_ALTITUDE.toFixed(7);
        ground_altitude=data.GROUND_ALTITUDE * 3.28084;
        ground_altitude=ground_altitude.toFixed(7);
        plane_pitch_degrees=radiansToDegrees(data.PLANE_PITCH_DEGREES);
        plane_pitch_degrees=plane_pitch_degrees.toFixed(7);
        plane_bank_degrees=radiansToDegrees(data.PLANE_BANK_DEGREES);
        plane_bank_degrees=plane_bank_degrees.toFixed(7);
        plane_heading_degrees_true=radiansToDegrees(data.PLANE_HEADING_DEGREES_TRUE);
        plane_heading_degrees_true=plane_heading_degrees_true.toFixed(7);
        plane_heading_degrees_magnetic=radiansToDegrees(data.PLANE_HEADING_DEGREES_MAGNETIC);
        plane_heading_degrees_magnetic=plane_heading_degrees_magnetic.toFixed(7);
        airspeed_indicated=data.AIRSPEED_INDICATED.toFixed(7);
        airspeed_true=data.AIRSPEED_TRUE.toFixed(7);
        ground_velocity=data.GROUND_VELOCITY.toFixed(7);
        vertical_speed=data.VERTICAL_SPEED.toFixed(7);
        incidence_beta=radiansToDegrees(data.INCIDENCE_BETA);
        incidence_beta=incidence_beta.toFixed(7);
        acceleration_body_x=data.ACCELERATION_BODY_X.toFixed(7);
        acceleration_body_y=data.ACCELERATION_BODY_Y.toFixed(7);
        acceleration_body_z=data.ACCELERATION_BODY_Z.toFixed(7);
        incidence_alpha=radiansToDegrees(data.INCIDENCE_ALPHA);
        incidence_alpha=incidence_alpha.toFixed(7);

        // Get current time
        let now = new Date();
        let timestamp = now.toISOString(); // ISO 8601 format, e.g., 2024-08-22T14:35:22.123Z

        // Data to be sent to the server
        let logData = {
            timestamp: timestamp,
            // 飞行高度Altitude:包括相对于海平面的高度（MSL）和相对于地面的高度（AGL）。大坡度盘旋时，通常会有高度的变化。
            plane_altitude,//feets
            ground_altitude,//feets
            //飞机俯仰角Pitch Angle:表示飞机的机头相对于地平线的角度。
            plane_pitch_degrees,//degrees
            //飞机滚转角Roll Angle:表示飞机相对于地平线的倾斜角度。大坡度盘旋通常伴随着较大的滚转角。
            plane_bank_degrees,//degrees
            //航向Heading:当前飞机的航向。
            plane_heading_degrees_true,//degrees
            plane_heading_degrees_magnetic,//degrees
            //指示空速（Indicated Airspeed, IAS），这是从空速表直接读出的速度，未校正误差。
            airspeed_indicated,//knots
            //真空速（True Airspeed, TAS），这是飞机相对于周围空气的真实速度
            airspeed_true,//knots
            //地速（Ground Speed），这是飞机相对于地面的速度
            ground_velocity,//knots
            //垂直速度Vertical Speed:表示飞机的爬升或下降速度。
            vertical_speed,//feet per second
            //侧滑角Sideslip Angle，偏航率Yaw Rate:这些数据能够帮助判断飞机是否处于协调转弯中。
            incidence_beta,//degrees
            //加速度Acceleration:包括纵向、横向和垂直方向的加速度数据。可以用于检测重力变化和其他动态情况。
            //表示沿飞机纵轴（前后方向）的加速度
            acceleration_body_x,//feet per second squared
            //表示沿飞机横轴（左右方向）的加速度
            acceleration_body_y,//feet per second squared
            //表示沿飞机竖轴（上下方向）的加速度
            acceleration_body_z,//feet per second squared
            //攻角Angle of Attack, AOA:表示机翼迎角，特别是在大坡度盘旋时，这个数据非常关键。
            incidence_alpha//radians
        };

        // Send data to server using AJAX
        $.ajax({
            url: $SCRIPT_ROOT + '/log_data',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(logData),  // Convert logData to JSON string
            success: function(response) {
                console.log("Data logged successfully:", response);
            },
            error: function(error) {
                console.error("Error logging data:", error);
            }
        });

        // Output data to the console with timestamp
        console.log("Simulator Data at " + timestamp + ":", {
            altitude,
            vertical_speed,
            compass,
            airspeed,
            latitude,
            longitude,
            fuel_percentage,
            autopilot_master,
            autopilot_nav_selected,
            autopilot_wing_leveler,
            autopilot_heading_lock,
            autopilot_heading_lock_dir,
            autopilot_altitude_lock,
            autopilot_altitude_lock_var,
            autopilot_attitude_hold,
            autopilot_glidescope_hold,
            autopilot_approach_hold,
            autopilot_backcourse_hold,
            autopilot_vertical_hold,
            autopilot_vertical_hold_var,
            autopilot_pitch_hold,
            autopilot_pitch_hold_ref,
            autopilot_flight_director_active,
            autopilot_airspeed_hold,
            autopilot_airspeed_hold_var,
            gear_handle_position,
            elevator_trim_pct,
            elevator_trim_pct_reversed,
            //rudder_trim_pct,
            flaps_handle_pct,
            flaps_handle_pct_reversed,
            cabin_no_smoking_alert_switch,
            cabin_seatbelts_alert_switch
        });

    });
    return false;
}

function radiansToDegrees(radians) {
    return radians * (180 / Math.PI);
}

function displayData() {
    //Navigation
    $("#altitude").text(altitude);
    $("#compass").text(compass);
    $("#vertical-speed").text(vertical_speed);
    $("#airspeed").text(airspeed);

    //Fuel
    $("#fuel-percentage").text(fuel_percentage);
    $("#fuel-percentage-bar").css("width", fuel_percentage+"%");

    //Autopilot
    checkAndUpdateButton("#autopilot-master", autopilot_master, "Engaged", "Disengaged");
    checkAndUpdateButton("#autopilot-wing-leveler", autopilot_wing_leveler);
    checkAndUpdateButton("#autopilot-heading-lock", autopilot_heading_lock);
    checkAndUpdateButton("#autopilot-altitude-lock", autopilot_altitude_lock);
    checkAndUpdateButton("#autopilot-airspeed-hold", autopilot_airspeed_hold);
    checkAndUpdateButton("#autopilot-attitude-hold", autopilot_attitude_hold);
    checkAndUpdateButton("#autopilot-backcourse-hold", autopilot_backcourse_hold);
    checkAndUpdateButton("#autopilot-approach-hold", autopilot_approach_hold);
    checkAndUpdateButton("#autopilot-vertical-hold", autopilot_vertical_hold);

    $("#autopilot-heading-lock-dir").attr('placeholder', autopilot_heading_lock_dir);
    $("#autopilot-altitude-lock-var").attr('placeholder', autopilot_altitude_lock_var);
    $("#autopilot-airspeed-hold-var").attr('placeholder', autopilot_airspeed_hold_var);
    $("#autopilot-pitch-hold-ref").attr('placeholder', autopilot_pitch_hold_ref);
    $("#autopilot-vertical-hold-ref").attr('placeholder', autopilot_vertical_hold_var);

    //Control surfaces
    $("#gear-handle-position").html(gear_handle_position);
    if (gear_handle_position === "UP"){
        $("#gear-handle-position").removeClass("btn-success").addClass("btn-danger");
    } else {
        $("#gear-handle-position").removeClass("btn-danger").addClass("btn-success");
    }

    $("#flaps-handle-pct").text(flaps_handle_pct);
    $("#flaps-slider").slider({values: [flaps_handle_pct_reversed]})

    $("#elevator-trim-pct").text(elevator_trim_pct);
    $("#elevator-trim-slider").slider({values: [elevator_trim_pct_reversed]})

    //$("#rudder-trim-pct").text(rudder_trim_pct);
    //$("#rudder-trim-slider").slider({values: [rudder_trim_pct]})

    //Cabin
    if (cabin_seatbelts_alert_switch === 1){
        $("#seatbelt-sign").removeClass("btn-outline-danger").addClass("btn-danger").html("Seatbelt sign on");
    } else {
        $("#seatbelt-sign").removeClass("btn-danger").addClass("btn-outline-danger").html("Seatbelt sign off");
    }

    if (cabin_no_smoking_alert_switch === 1){
        $("#no-smoking-sign").removeClass("btn-outline-danger").addClass("btn-danger").html("No smoking sign on");
    } else {
        $("#no-smoking-sign").removeClass("btn-danger").addClass("btn-outline-danger").html("No smoking sign off");
    }}

function checkAndUpdateButton(buttonName, variableToCheck, onText="On", offText="Off") {
    if (variableToCheck === 1) {
        $(buttonName).removeClass("btn-danger").addClass("btn-success").html(onText);
    } else {
        $(buttonName).removeClass("btn-success").addClass("btn-danger").html(offText);
    }
}


function toggleFollowPlane() {
    followPlane = !followPlane;
    if (followPlane === true) {
        $("#followMode").text("Moving map enabled")
        $("#followModeButton").removeClass("btn-outline-danger").addClass("btn-primary")
    }
    if (followPlane === false) {
        $("#followMode").text("Moving map disabled")
        $("#followModeButton").removeClass("btn-primary").addClass("btn-outline-danger")
    }
}

function updateMap() {
    var pos = L.latLng(latitude, longitude);

    marker.slideTo(	pos, {
        duration: 1500,
    });
    marker.setRotationAngle(compass);

    if (followPlane === true) {
        map.panTo(pos);
    }
}

function setSimDatapoint(datapointToSet, valueToUse) {
    url_to_call = "/datapoint/"+datapointToSet+"/set";
    $.post( url_to_call, { value_to_use: valueToUse } );
}

function triggerSimEvent(eventToTrigger, valueToUse, hideAlert = false){
    url_to_call = "/event/"+eventToTrigger+"/trigger";
    $.post( url_to_call, { value_to_use: valueToUse } );

    if (!hideAlert) {
        temporaryAlert('', "Sending instruction", "success")
    }
}

function triggerSimEventFromField(eventToTrigger, fieldToUse, messageToDisplay = null){
    // Get the field and the value in there
    fieldToUse = "#" + fieldToUse
    valueToUse = $(fieldToUse).val();

    // Pass it to the API
    url_to_call = "/event/"+eventToTrigger+"/trigger";
    $.post( url_to_call, { value_to_use: valueToUse } );

    // Clear the field so it can be repopulated with the placeholder
    $(fieldToUse).val("")

    if (messageToDisplay) {
        temporaryAlert('', messageToDisplay + " to " + valueToUse, "success")
    }

}

function triggerCustomEmergency(emergency_type) {
    url_to_call = "/custom_emergency/" + emergency_type
    $.post (url_to_call)

    if (emergency_type === "random_engine_fire") {
        temporaryAlert("Fire!", "Random engine fire trigger sent", "error")
    }
}


function temporaryAlert(title, message, icon) {
    let timerInterval

    Swal.fire({
        title: title,
        html: message,
        icon: icon,
        timer: 1000,
        timerProgressBar: true,
        onBeforeOpen: () => {
            Swal.showLoading()
            timerInterval = setInterval(() => {
                const content = Swal.getContent()
                if (content) {
                    const b = content.querySelector('b')
                    if (b) {
                        b.textContent = Swal.getTimerLeft()
                    }
                }
            }, 100)
        },
        onClose: () => {
            clearInterval(timerInterval)
        }
    }).then((result) => {
        /* Read more about handling dismissals below */
        if (result.dismiss === Swal.DismissReason.timer) {
            console.log('I was closed by the timer')
        }
    })
}