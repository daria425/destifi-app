import { Popover } from "@radix-ui/themes";

export default function SearchPopover({ options }) {
  return (
    <Popover.Root>
      <Popover.Content>
        <ul>
          {options.map((option, index) => (
            <li key={index}>{option}</li>
          ))}
        </ul>
      </Popover.Content>
    </Popover.Root>
  );
}
