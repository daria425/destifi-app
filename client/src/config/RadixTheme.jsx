import { Theme } from "@radix-ui/themes";

export default function RadixTheme({ children }) {
  return (
    <Theme accentColor="iris" grayColor="mauve">
      {children}
    </Theme>
  );
}
