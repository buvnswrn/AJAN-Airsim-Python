
class MQTT:
    DOMAIN = "mqtt.mrk40.dfki.lan"
    PROTOCOL = "mqtt"
    TCP_PORT = 1883
    WEBSOCKET_PORT = 8083
    DRONE_MODEL: str = "Mavic2"
    LIVE_IMAGE_URL = "http://pixel1.mrk40.dfki.lan:8080/image.jpg"
    class SUBSCRIBE_CHANNELS:
        DRONE_MODEL: str = "Mavic2"
        STATE: str = DRONE_MODEL+"/state/"
        COMMAND = DRONE_MODEL+"/command/"
        RES = "/res"
        CONNECTION = STATE + "connection"  # Called on connection changes
        POSE = STATE + "pose"  # The topic on which measured pose values come in.
        GOALS = STATE + "goals"  # Inform about current goals.

        FLIGHT_PHASE = STATE + "flightPhase"  # Phase Idle - Waiting for input. Phase 0 - Turning the drone towards
        # the goal. Phase 1 - Flying towards the goal. Phase 2 - Turning the drone to the desired end rotation.

        DELTA = STATE + "delta"  # Delta time = App-ingoing pose timestamp - OptiTrack capture timestamp (for benchmark
        # purpose only).

        PHYSICAL = STATE + "physical"  # Represents the physical state of the aircraft.

        RTMP = STATE + "RTMP"  # Represents the RTMP stream state.
        
        MOVE_TO_KNOWN_POSITION = COMMAND + 'moveToKnownPosition'+ RES

        MOVE_TO_POINT = COMMAND + "moveToPoint" + RES
        MOVE_TO_WAY_POINTS = COMMAND + "moveToWaypoints" + RES
        startLiveImage = COMMAND + "startLiveImage" + RES
        stopLiveImage = COMMAND + "stopLiveImage" + RES
        startRTMPStream = COMMAND + "startRTMPStream" + RES
        stopRTMPStream = COMMAND + "stopRTMPStream" + RES
        TAKE_OFF_AND_HANDOVER_CONTROL = COMMAND + "takeOffAndHandOverControl" + RES
        pauseMotion = COMMAND + "pauseMotion" + RES
        continueMotion = COMMAND + "continueMotion" + RES
        emergencyLanding = COMMAND + "emergencyLanding" + RES
        setPIDGains = COMMAND + "setPIDGains" + RES

    class PUBLISH_CHANNELS:
        DRONE_MODEL: str = "Mavic2"
        COMMAND: str = DRONE_MODEL + "/command/"
        REQ: str = "/req"

        MOVE_TO_POSITION = COMMAND + "moveToKnownPosition" + REQ  # Move drone to a known position saved in the World
        # Model Server.
        MOVE_TO_KNOWN_POSITION = COMMAND + "moveToKnownPosition" + REQ  # Response to inform about status.

        MOVE_TO_POINT = COMMAND + "moveToPoint" + REQ
        MOVE_TO_WAYPOINTS = COMMAND + "moveToWaypoints" + REQ
        startLiveImage = COMMAND + "startLiveImage" + REQ
        stopLiveImage = COMMAND + "stopLiveImage" + REQ
        startRTMPStream = COMMAND + "startRTMPStream" + REQ
        stopRTMPStream = COMMAND + "stopRTMPStream" + REQ
        TAKE_OFF_AND_HAND_OVER_CONTROL = COMMAND + "takeOffAndHandOverControl" + REQ
        pauseMotion = COMMAND + "pauseMotion" + REQ
        continueMotion = COMMAND + "continueMotion" + REQ
        emergencyLanding = COMMAND + "emergencyLanding" + REQ
        setPIDGains = COMMAND + "setPIDGains" + REQ

    class PHYSICAL:
        HOVERING = "HOVERING"
        ONGROUND = "ONGROUND"
        TAKINGOFF = "TAKINGOFF"
        MOVING = "MOVING"
        LANDING = "LANDING"


