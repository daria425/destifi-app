import { Popover, Text } from "@radix-ui/themes";

export default function SearchPopover({ options }) {
  return (
    <ul className="search-popover">
      {options.map((option, index) => (
        <li key={index} className="search-popover__item">
          <Text as="p" size={"1"} weight="bold">
            {option.label}
          </Text>
          {option.description && (
            <Text as="p" size={"1"} color="gray" wrap={false} truncate>
              {option.description}
            </Text>
          )}
        </li>
      ))}
    </ul>
  );
}
