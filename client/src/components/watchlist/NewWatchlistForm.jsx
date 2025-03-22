import DialogForm from "../common/DialogForm";
import WatchlistFormInput from "./WatchlistFormInput";
export default function NewWatchlistForm({ uid }) {
  return (
    <DialogForm title={"Create Watchlist"}>
      <WatchlistFormInput uid={uid} />
    </DialogForm>
  );
}
