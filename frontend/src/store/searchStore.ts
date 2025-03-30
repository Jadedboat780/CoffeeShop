import { getCoffeeList } from "@/store/coffeeStore.ts";
import { type StateCreator, create } from "zustand";

type State = {
	text?: string;
};

type Action = {
	setText: (text: string) => void;
};

const SearchSlice: StateCreator<State & Action> = (set) => ({
	text: undefined,
	setText: (text) => {
		set({ text: text });
	},
});

export const useSearchStore = create<State & Action>(SearchSlice);
export const setSearchText = (text: string) => useSearchStore.getState().setText(text);

useSearchStore.subscribe((state, prevState) => {
	if (state.text !== prevState.text) {
		getCoffeeList({ text: state.text?.toLowerCase() });
	}
});
