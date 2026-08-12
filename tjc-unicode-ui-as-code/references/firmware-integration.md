# Firmware integration contract

Separate three layers:

1. raw HMI traffic and touch evidence;
2. presentation/display bindings;
3. authorized application commands.

## Display path

- Freeze page, object, property, source field, formatting, invalid text, and update policy in a display map.
- Make the MCU Presenter and HMI object inventory match exactly.
- Show MCU-confirmed state for commands and actuators; do not use a button's private local value as final truth.
- Prefer blank or neutral defaults, or preload snapshots, so page entry does not flash from fake data to real data.

## Touch path

- Use release events for committed actions unless the product contract explicitly requires press behavior.
- Record raw touch frames for diagnostics without automatically converting them into application commands.
- Keep navigation, number editing, RTC field changes, and test hotspots local when appropriate while still emitting raw release evidence.
- Translate only a page/component/event whitelist into business commands.
- Keep the component-ID gate disabled until real-panel IDs have been exported and compared with zero differences.

## Safety path

- Never let UI text or button availability silently bypass firmware safety or commissioning gates.
- Keep heater, mains, relays, ionizers, and other hazardous outputs independently locked until hardware polarity, connector, and low-voltage commissioning evidence exists.
- Record pending gates in both firmware configuration and HMI release status.

## Acceptance evidence

For every enabled command, retain:

- raw page/component/event evidence;
- command mapping and argument validation;
- MCU acknowledgement and confirmed-state writeback;
- UI state after success, rejection, timeout, and reconnect;
- parser, ring, UART, malformed-command, and ACK-timeout counters.

