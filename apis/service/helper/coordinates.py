import math


def relative_to_global(current_position, current_yaw, move_x, move_y, move_z):
    """
    :param move_z:
    :param move_y:
    :param move_x:
    :param current_position:
    :param current_yaw:
    :return: x, y z values relative to global coordinates
    """
    radians_yaw = current_yaw / 180 * math.pi
    _x = move_x * math.cos(radians_yaw) + move_y * math.cos(radians_yaw + math.pi / 2) + current_position.x_val
    _y = move_x * math.sin(radians_yaw) + move_y * math.sin(radians_yaw + math.pi / 2) + current_position.y_val
    _z = move_z
    return _x, _y, _z


def quaternion_to_euler_angle(q):
    """
    :param q:
    :return: roll, pitch, yaw in euler angles
    """
    sinr_cosp = 2 * (q.w_val * q.x_val + q.y_val * q.z_val)
    cosr_cosp = 1 - 2 * (q.x_val * q.x_val + q.y_val * q.y_val)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2 * (q.w_val * q.y_val - q.z_val * q.x_val)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp)  # use 90 degrees if out of range
    else:
        pitch = math.asin(sinp)

    siny_cosp = 2 * (q.w_val * q.z_val + q.x_val * q.y_val)
    cosy_cosp = 1 - 2 * (q.y_val * q.y_val + q.z_val * q.z_val)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


def get_airsim_values(unity_x, unity_y, unity_z):
    """
    :param unity_x:
    :param unity_y:
    :param unity_z:
    :return: airsim values
    """
    return unity_z, unity_x, -unity_y


def get_unity_values(airsim_x, airsim_y, airsim_z):
    """
    :param airsim_x:
    :param airsim_y:
    :param airsim_z:
    :return: unity values
    """
    return airsim_y, -airsim_z, airsim_x
