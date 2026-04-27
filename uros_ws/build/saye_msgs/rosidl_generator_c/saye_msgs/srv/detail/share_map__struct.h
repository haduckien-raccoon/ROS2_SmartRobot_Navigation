// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from saye_msgs:srv/ShareMap.idl
// generated code does not contain a copyright notice

#ifndef SAYE_MSGS__SRV__DETAIL__SHARE_MAP__STRUCT_H_
#define SAYE_MSGS__SRV__DETAIL__SHARE_MAP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'topic_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ShareMap in the package saye_msgs.
typedef struct saye_msgs__srv__ShareMap_Request
{
  rosidl_runtime_c__String topic_name;
} saye_msgs__srv__ShareMap_Request;

// Struct for a sequence of saye_msgs__srv__ShareMap_Request.
typedef struct saye_msgs__srv__ShareMap_Request__Sequence
{
  saye_msgs__srv__ShareMap_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} saye_msgs__srv__ShareMap_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'custom_occupany_grid'
#include "nav_msgs/msg/detail/occupancy_grid__struct.h"
// Member 'status_message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ShareMap in the package saye_msgs.
typedef struct saye_msgs__srv__ShareMap_Response
{
  bool is_completed;
  nav_msgs__msg__OccupancyGrid custom_occupany_grid;
  rosidl_runtime_c__String status_message;
} saye_msgs__srv__ShareMap_Response;

// Struct for a sequence of saye_msgs__srv__ShareMap_Response.
typedef struct saye_msgs__srv__ShareMap_Response__Sequence
{
  saye_msgs__srv__ShareMap_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} saye_msgs__srv__ShareMap_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SAYE_MSGS__SRV__DETAIL__SHARE_MAP__STRUCT_H_
