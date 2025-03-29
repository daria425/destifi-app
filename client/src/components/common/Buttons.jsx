import { Button, IconButton } from "@radix-ui/themes";

import { Cross2Icon } from "@radix-ui/react-icons";
function PrimaryButton({
  children,
  onClick,
  type = "button",
  disabled = false,
}) {
  return (
    <Button onClick={onClick} variant="solid" type={type} disabled={disabled}>
      {children}
    </Button>
  );
}

function SecondaryButton({
  children,
  onClick,
  type = "button",
  disabled = false,
}) {
  return (
    <Button
      onClick={onClick}
      color="gray"
      variant="soft"
      type={type}
      disabled={disabled}
      highContrast
    >
      {children}
    </Button>
  );
}

function CloseButton({ onClick, iconProps }) {
  return (
    <IconButton onClick={onClick} variant="ghost">
      <Cross2Icon {...iconProps} />
    </IconButton>
  );
}
export { PrimaryButton, SecondaryButton, CloseButton };
