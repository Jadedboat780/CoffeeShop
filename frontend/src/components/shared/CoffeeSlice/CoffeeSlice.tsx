import {useCoffeeStore} from "@/store";
import {useEffect} from "react";
import {CoffeeCard} from "@/components/shared";
import styles from './CoffeeSlice.module.css'


export const CoffeeSlice = () => {
    const {coffeeList, getCoffeeList} = useCoffeeStore()
    useEffect(() => {
        getCoffeeList()
    }, [])

    return <div className={styles.slice}>
        {coffeeList ?
            coffeeList.map((coffee) => <CoffeeCard key={coffee.id} {...coffee}/>)
            : <span>Coffee no found :(</span>
        }
    </div>
}
