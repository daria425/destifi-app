import { Popover } from "@radix-ui/themes";
import { useState } from "react";
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
