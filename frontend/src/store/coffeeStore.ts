import type { CoffeeItem, CoffeeQueryParams } from "@/types/coffee.ts";
import axios from "axios";
import { type StateCreator, create } from "zustand";

const URL = "https://purpleschool.ru/coffee-api/";

type State = {
	coffeeList: CoffeeItem[];
	controller?: AbortController;
};

type Action = {
	getCoffeeList: (params?: CoffeeQueryParams) => void;
};

const coffeeSlice: StateCreator<State & Action> = (set, get) => ({
	coffeeList: [],
	controller: undefined,
	getCoffeeList: async (params) => {
		const { controller } = get();

		if (controller) {
			controller.abort();
		}

		const newController = new AbortController();
		set({ controller: newController });
		const { signal } = newController;

		try {
			const { data } = await axios.get<CoffeeItem[]>(URL, { params, signal });
			set({ coffeeList: data });
		} catch (err) {
			if (axios.isCancel(err)) {
				return;
			}
			console.log(err);
		}
	},
});

export const useCoffeeStore = create<State & Action>(coffeeSlice);
export const getCoffeeList = (params?: CoffeeQueryParams) => useCoffeeStore.getState().getCoffeeList(params);
