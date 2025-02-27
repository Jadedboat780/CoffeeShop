import {create, StateCreator} from 'zustand'
import axios from 'axios'
import {CoffeeItem, CoffeeQueryParams} from "@/types/coffee.ts";

const URL = "https://purpleschool.ru/coffee-api/"

type CoffeeState = {
    coffeeList?: CoffeeItem[],
    controller?: AbortController
}

type CoffeeActions = {
    getCoffeeList: (params?: CoffeeQueryParams) => void
}

const coffeeSlice: StateCreator<CoffeeState & CoffeeActions> = (set, get) => ({
    coffeeList: undefined,
    controller: undefined,
    getCoffeeList: async (params) => {
        const {controller} = get();

        if (controller) {
            controller.abort();
        }

        const newController = new AbortController();
        set({controller: newController});
        const {signal} = newController;

        try {
            const {data} = await axios.get(URL, {params, signal});
            set({coffeeList: data})
        } catch (err) {
            if (axios.isCancel(err)) {
                return
            }
            console.log(err)
        }
    }
})

export const useCoffeeStore = create<CoffeeState & CoffeeActions>(coffeeSlice)
export const getCoffeeList = (params?: CoffeeQueryParams) => useCoffeeStore.getState().getCoffeeList(params)