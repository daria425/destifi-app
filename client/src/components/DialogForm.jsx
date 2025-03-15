import * as Dialog from "@radix-ui/react-dialog";
import RadixTheme from "../config/RadixTheme";
export default function DialogForm({ title, children }) {
  return (
    <Dialog.Root open={true} className="dialog-root">
      <Dialog.Portal>
        <RadixTheme>
          <Dialog.Overlay className="dialog-overlay" />
          <Dialog.Content
            className="dialog-content"
            aria-describedby={"dialog-form"}
            aria-labelledby="dialog-form"
          >
            <Dialog.Title className="dialog-title">{title}</Dialog.Title>
            {children}
          </Dialog.Content>
        </RadixTheme>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
