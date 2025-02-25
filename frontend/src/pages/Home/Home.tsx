import {SearchBar, CoffeeSlice} from "@/components/shared";

import {ListCoffeeItem} from "@/types/coffee";

const data: ListCoffeeItem = [
    {
        id: 1,
        title: 'Frappe',
        description: 'sdujjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',
        price: 150,
        image_url: './frappe.png',
    },
    {
        id: 2,
        title: 'Frappe',
        description: 'sdujjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',
        price: 150,
        image_url: './frappe.png',
    },
    {
        id: 3,
        title: 'Frappe',
        description: 'sdujjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',
        price: 150,
        image_url: './frappe.png',
    },
    {
        id: 4,
        title: 'Frappe',
        description: 'sdujjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',
        price: 150,
        image_url: './frappe.png',
    },
]

export const Home = () => {
    return <div>
        <SearchBar/>
        <br/>
        <CoffeeSlice coffeeList={data}/>
    </div>
}