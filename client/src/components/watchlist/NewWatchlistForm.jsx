import DialogForm from "../common/DialogForm";
import WatchlistFormInput from "./WatchlistFormInput";
export default function NewWatchlistForm({ uid, formOpen, dialogCloseButton }) {
  return (
    <DialogForm
      title={"Create Watchlist"}
      dialogOpen={formOpen}
      dialogCloseButton={dialogCloseButton}
    >
      <WatchlistFormInput uid={uid} />
    </DialogForm>
  );
}
