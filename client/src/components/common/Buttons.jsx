import { Button } from "@radix-ui/themes";
function PrimaryButton({ children, onClick, type = "button" }) {
  return (
    <Button onClick={onClick} variant="solid" type={type}>
      {children}
    </Button>
  );
}

function SecondaryButton({ children, onClick, type = "button" }) {
  return (
    <Button
      onClick={onClick}
      color="gray"
      variant="soft"
      type={type}
      highContrast
    >
      {children}
    </Button>
  );
}

export { PrimaryButton, SecondaryButton };
