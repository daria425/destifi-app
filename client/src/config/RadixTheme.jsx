import { Theme } from "@radix-ui/themes";

export default function RadixTheme({ children }) {
  return (
    <Theme accentColor="gold" grayColor="sand">
      {children}
    </Theme>
  );
}
