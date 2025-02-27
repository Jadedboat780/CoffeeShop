import {create, StateCreator} from "zustand";
import {getCoffeeList} from "@/store/coffeeStore.ts";

type SearchState = {
    text?: string
    setText: (text: string) => void
}

const SearchSlice: StateCreator<SearchState> = (set) => ({
    text: undefined,
    setText: (text) => {
        set({text: text})
    }
})

export const useSearchStore = create<SearchState>(SearchSlice)

useSearchStore.subscribe((state, prevState) => {
    if (state.text !== prevState.text) {
        getCoffeeList({text: state.text?.toLowerCase()})
    }
})