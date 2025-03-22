import { Text } from "@radix-ui/themes";
import { mauve } from "@radix-ui/colors";
export default function InputLabel({ labelText, inputId }) {
  return (
    <Text
      as="label"
      size={"2"}
      weight={"bold"}
      htmlFor={inputId}
      color={mauve.mauve11}
    >
      {labelText}
    </Text>
  );
}
