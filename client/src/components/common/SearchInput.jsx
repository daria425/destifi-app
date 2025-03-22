import { TextField } from "@radix-ui/themes";
export default function SearchInput({
  searchHandler,
  focusHandler,
  searchValue,
  textFieldProps,
}) {
  return (
    <TextField.Root
      {...textFieldProps}
      value={searchValue}
      onChange={(e) => searchHandler(e)}
      onFocus={focusHandler}
      onBlur={focusHandler}
    ></TextField.Root>
  );
}
