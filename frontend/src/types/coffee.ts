export type CoffeeCategory = 'cappuccino' | 'latte' | 'macchiato' | 'americano'

export type CoffeeItem = {
    id: number
    name: string // title
    description: string
    price: number
    type: CoffeeCategory // category
    image: string
}

export type CoffeeQueryParams = {
    text?: string
}
