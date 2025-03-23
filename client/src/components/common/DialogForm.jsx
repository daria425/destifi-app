import * as Dialog from "@radix-ui/react-dialog";
import { Flex } from "@radix-ui/themes";
import RadixTheme from "../../config/RadixTheme";
export default function DialogForm({
  title,
  children,
  dialogOpen,
  dialogCloseButton,
}) {
  return (
    <Dialog.Root className="dialog-root" open={dialogOpen}>
      <Dialog.Portal>
        <RadixTheme>
          <Dialog.Overlay className="dialog-overlay" />
          <Dialog.Content
            className="dialog-content"
            aria-describedby={undefined}
            aria-labelledby="dialog-form"
          >
            <Flex justify={"between"} align={"center"}>
              <Dialog.Title className="dialog-title">{title}</Dialog.Title>
              {dialogCloseButton}
            </Flex>
            {children}
          </Dialog.Content>
        </RadixTheme>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
