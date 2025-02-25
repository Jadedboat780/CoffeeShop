import {CoffeeCard} from "@/components/shared";
import {ListCoffeeItem} from "@/types/coffee";
import styles from './CoffeeSlice.module.css'


export const CoffeeSlice = ({ coffeeList }: { coffeeList: ListCoffeeItem }) => {
    return <div className={styles.slice}>
        {coffeeList.map((coffee) => (<CoffeeCard key={coffee.id} {...coffee} />))}
        {coffeeList.map((coffee) => (<CoffeeCard key={coffee.id} {...coffee} />))}
    </div>
}
