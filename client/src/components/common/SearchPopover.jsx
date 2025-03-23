import { Popover, Text } from "@radix-ui/themes";
import { CheckIcon } from "@radix-ui/react-icons";
export default function SearchPopover({ options, selectHandler, isAdded }) {
  return (
    <ul className="search-popover">
      {options.map((option, index) => (
        <li
          key={index}
          className={`search-popover__item ${
            isAdded(option) ? "search-popover__item--added" : ""
          }`}
          onClick={() => selectHandler(option)}
        >
          <Text as="p" size={"1"} weight="bold">
            {option.label}
          </Text>
          {option.description && (
            <Text as="p" size={"1"} color="gray" wrap={false} truncate>
              {option.description}
            </Text>
          )}
          {isAdded(option) && (
            <CheckIcon height={20} width={20} className="check-icon" />
          )}
        </li>
      ))}
    </ul>
  );
}
