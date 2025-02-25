export type CoffeeCategory = 'cappuccino' | 'latte' | 'macchiato' | 'americano'
export type CoffeeSize = 's' | 'm' | 'l'

export type CoffeeItem = {
    id: number
    title: string
    description: string
    price: number
    image_url: string
}

export type ListCoffeeItem = CoffeeItem[]
