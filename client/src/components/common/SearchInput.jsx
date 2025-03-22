import { TextField } from "@radix-ui/themes";
export default function SearchInput({
  searchHandler,
  searchValue,
  textFieldProps,
}) {
  console.log(searchValue);
  return (
    <TextField.Root
      {...textFieldProps}
      value={searchValue}
      onChange={(e) => searchHandler(e)}
    ></TextField.Root>
  );
}
