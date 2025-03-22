import { TextField } from "@radix-ui/themes";
export default function SearchInput({
  searchHandler,
  searchValue,
  textFieldProps,
}) {
  return (
    <TextField
      {...textFieldProps}
      value={searchValue}
      onChange={(e) => searchHandler(e.target.value)}
    />
  );
}
