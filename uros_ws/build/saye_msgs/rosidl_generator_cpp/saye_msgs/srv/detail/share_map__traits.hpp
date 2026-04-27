// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from saye_msgs:srv/ShareMap.idl
// generated code does not contain a copyright notice

#ifndef SAYE_MSGS__SRV__DETAIL__SHARE_MAP__TRAITS_HPP_
#define SAYE_MSGS__SRV__DETAIL__SHARE_MAP__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "saye_msgs/srv/detail/share_map__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace saye_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ShareMap_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: topic_name
  {
    out << "topic_name: ";
    rosidl_generator_traits::value_to_yaml(msg.topic_name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ShareMap_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: topic_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "topic_name: ";
    rosidl_generator_traits::value_to_yaml(msg.topic_name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ShareMap_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace saye_msgs

namespace rosidl_generator_traits
{

[[deprecated("use saye_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const saye_msgs::srv::ShareMap_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  saye_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use saye_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const saye_msgs::srv::ShareMap_Request & msg)
{
  return saye_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<saye_msgs::srv::ShareMap_Request>()
{
  return "saye_msgs::srv::ShareMap_Request";
}

template<>
inline const char * name<saye_msgs::srv::ShareMap_Request>()
{
  return "saye_msgs/srv/ShareMap_Request";
}

template<>
struct has_fixed_size<saye_msgs::srv::ShareMap_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<saye_msgs::srv::ShareMap_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<saye_msgs::srv::ShareMap_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'custom_occupany_grid'
#include "nav_msgs/msg/detail/occupancy_grid__traits.hpp"

namespace saye_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ShareMap_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: is_completed
  {
    out << "is_completed: ";
    rosidl_generator_traits::value_to_yaml(msg.is_completed, out);
    out << ", ";
  }

  // member: custom_occupany_grid
  {
    out << "custom_occupany_grid: ";
    to_flow_style_yaml(msg.custom_occupany_grid, out);
    out << ", ";
  }

  // member: status_message
  {
    out << "status_message: ";
    rosidl_generator_traits::value_to_yaml(msg.status_message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ShareMap_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: is_completed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_completed: ";
    rosidl_generator_traits::value_to_yaml(msg.is_completed, out);
    out << "\n";
  }

  // member: custom_occupany_grid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "custom_occupany_grid:\n";
    to_block_style_yaml(msg.custom_occupany_grid, out, indentation + 2);
  }

  // member: status_message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status_message: ";
    rosidl_generator_traits::value_to_yaml(msg.status_message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ShareMap_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace saye_msgs

namespace rosidl_generator_traits
{

[[deprecated("use saye_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const saye_msgs::srv::ShareMap_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  saye_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use saye_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const saye_msgs::srv::ShareMap_Response & msg)
{
  return saye_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<saye_msgs::srv::ShareMap_Response>()
{
  return "saye_msgs::srv::ShareMap_Response";
}

template<>
inline const char * name<saye_msgs::srv::ShareMap_Response>()
{
  return "saye_msgs/srv/ShareMap_Response";
}

template<>
struct has_fixed_size<saye_msgs::srv::ShareMap_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<saye_msgs::srv::ShareMap_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<saye_msgs::srv::ShareMap_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<saye_msgs::srv::ShareMap>()
{
  return "saye_msgs::srv::ShareMap";
}

template<>
inline const char * name<saye_msgs::srv::ShareMap>()
{
  return "saye_msgs/srv/ShareMap";
}

template<>
struct has_fixed_size<saye_msgs::srv::ShareMap>
  : std::integral_constant<
    bool,
    has_fixed_size<saye_msgs::srv::ShareMap_Request>::value &&
    has_fixed_size<saye_msgs::srv::ShareMap_Response>::value
  >
{
};

template<>
struct has_bounded_size<saye_msgs::srv::ShareMap>
  : std::integral_constant<
    bool,
    has_bounded_size<saye_msgs::srv::ShareMap_Request>::value &&
    has_bounded_size<saye_msgs::srv::ShareMap_Response>::value
  >
{
};

template<>
struct is_service<saye_msgs::srv::ShareMap>
  : std::true_type
{
};

template<>
struct is_service_request<saye_msgs::srv::ShareMap_Request>
  : std::true_type
{
};

template<>
struct is_service_response<saye_msgs::srv::ShareMap_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // SAYE_MSGS__SRV__DETAIL__SHARE_MAP__TRAITS_HPP_
