'use client'

import Image from 'next/image'
import { useReducer } from 'react'
import { Sheet } from 'react-modal-sheet'
import 'react-spring-bottom-sheet/dist/style.css'


import { CircleMinus, CirclePlus } from 'lucide-react'
import styles from './MobileProductPopUp.module.scss'

type PopUpProps = {
    product: {
        tableName: string
        itemId: number
        name: string
        img: string
        description: string
        price: number
        status: boolean
        type: "by weight" | "by portion"
    },
    closePopUp: () => void
}

type AdditionsProps = {
    "amount": number
    "quantity": number
    "weight": number
    "additions": {
        "cutlery": number
        "onion": number
        "cream": number
    }
}

type NestedField = {
    field: "additions"
    subField: keyof AdditionsProps["additions"]
}

type PopUpDataAction =
    | { type: "increment" | "decrement", field: keyof AdditionsProps; price: number }
    | ({ type: "increment" | "decrement", price: number } & NestedField)
    | { type: "updateWeight", field: Partial<AdditionsProps>, price: number }
    | { type: "update", field: Partial<AdditionsProps> }

const reducer = (state: AdditionsProps, action: PopUpDataAction): AdditionsProps => {
    switch (action.type) {
        case "increment":
            if (action.field === "additions" && "subField" in action) {
                return {
                    ...state,
                    additions: {
                        ...state.additions,
                        [action.subField]: state.additions[action.subField] + 1
                    },
                    amount: state.amount + 2
                }
            }
            else if (action.field === "weight") {
                const newWeight = Math.max(0, state.weight + 100)
                const weightPrice = newWeight * action.price
                const additionAmount = state.amount - (state.weight * action.price)
                return {
                    ...state,
                    weight: newWeight,
                    amount: weightPrice + additionAmount
                }
            }

            return {
                ...state,
                [action.field]: (state[action.field] as number) + 1,
                amount: state.amount + action.price
            }
        case "decrement":

            if (action.field === "additions" && "subField" in action) {
                return {
                    ...state,
                    additions: {
                        ...state.additions,
                        [action.subField]: state.additions[action.subField] - 1
                    },
                    amount: state.amount - 2
                }
            }
            else if (action.field === "weight") {
                const newWeight = Math.max(0, state.weight - 100)
                const weightPrice = newWeight * action.price
                const additionAmount = state.amount - (state.weight * action.price)
                return {
                    ...state,
                    weight: newWeight,
                    amount: weightPrice + additionAmount
                }
            }
            return {
                ...state,
                [action.field]: Math.max(0, (state[action.field] as number) - 1),
                amount: state.amount - action.price
            }
        case "updateWeight":
            return {
                ...state,
                ...action.field,
                amount: action.price * Number(action.field.weight)
            }
        default:
            return state
    }
}

const AdditionBtnLIst = [
    "cutlery",
    "onion",
    "cream",
]

export default function MobileProductPopUp({ product, closePopUp }: PopUpProps) {
    // const [productWeightToShow, setProductWeightToShow] = useState(0)

    const [productData, setAdditionData] = useReducer(reducer, {
        amount: product.price,
        quantity: 1,
        weight: 100,
        additions: {
            cutlery: 0,
            onion: 0,
            cream: 0
        }
    })


    const PopUpFooter = () => (
        <div className={styles.footerPopUp}>
            <div className={styles.footerContainer}>
                <div className={styles.infoAmount}>
                    <span>Total amount:<br></br> {productData.amount} </span>
                </div>
                <div className={styles.addBtnContainer}>
                    <button
                        disabled={!product.status}
                        className={styles.addToBasketBtn}
                        onClick={() => {
                            const newProductData = {
                                product,
                                "productData": productData
                            }

                            const basket = JSON.parse(localStorage.getItem("basket") || "{}")
                            if (basket[product.name]) {
                                basket[product.name].productData = {
                                    amount: basket[product.name].productData.amount + productData.amount,
                                    quantity: basket[product.name].productData.quantity + productData.quantity,
                                    weight: basket[product.name].productData.weight + productData.weight,
                                    additions: {
                                        cutlery: basket[product.name].productData.additions.cutlery + productData.additions.cutlery,
                                        onion: basket[product.name].productData.additions.onion + productData.additions.onion,
                                        cream: basket[product.name].productData.additions.cream + productData.additions.cream
                                    }
                                }
                            } else {
                                basket[product.name] = newProductData
                            }

                            localStorage.setItem("basket", JSON.stringify(basket))
                            window.dispatchEvent(new Event("basketUpdated"))
                            closePopUp()
                        }}
                    >
                        <span>
                            Add to basket
                        </span>
                    </button>
                </div>
            </div>
        </div>
    )

    if (!product) return null
    return (

        <>
            <Sheet
                isOpen={true}
                onClose={closePopUp}
                snapPoints={[0.8]}
                dragCloseThreshold={0.3}
            >
                <Sheet.Container>
                    <Sheet.Header></Sheet.Header>
                    <Sheet.Content>
                        <Sheet.Scroller>
                            <div style={{ zIndex: 15 }} className={styles.popUpContainer}>
                                <div className={styles.scrollContainer}>
                                    <div className={styles.product}>
                                        <div className={styles.productImg}>
                                            <div className={styles.imgContainer}>
                                                <Image src={product.img} alt={''} width={500} height={300} />
                                            </div>
                                        </div>
                                        <div className={styles.productInfo}>
                                            <div className={styles.infoContainer}>
                                                <h2>{product.name}</h2>
                                                <p>{product.description}</p>
                                            </div>
                                        </div>
                                        <div className={styles.additions}>
                                            <div className={styles.additionsContainer}>
                                                <div className={styles.productCounter}>
                                                    {product.type === "by portion" ?
                                                        <div className={styles.btnContainer}>
                                                            <button disabled={
                                                                productData.quantity === 0
                                                            } onClick={() => setAdditionData({ type: "decrement", field: "quantity", price: product.price })}>
                                                                <CircleMinus size={32} />
                                                            </button>
                                                            <span>{productData.quantity}</span>
                                                            <button onClick={() => setAdditionData({ type: "increment", field: "quantity", price: product.price })}
                                                            >
                                                                <CirclePlus size={32} />
                                                            </button>
                                                        </div> :
                                                        product.type === "by weight" &&
                                                        <div className={styles.btnContainer}>
                                                            <button disabled={
                                                                productData.quantity === 0
                                                            } onClick={() => setAdditionData({ type: "decrement", field: "weight", price: product.price })}>
                                                                <CircleMinus size={32} />
                                                            </button>
                                                            <span>{productData.weight}</span>
                                                            <button onClick={() => setAdditionData({ type: "increment", field: "weight", price: product.price })}
                                                            >
                                                                <CirclePlus size={32} />
                                                            </button>
                                                        </div>
                                                    }
                                                    <div className={styles.additionInformation}>
                                                        <span className={product.type === "by portion" ? styles.byPortionPrice : styles.byWeightPrice}>{product.price}</span>
                                                    </div>
                                                </div>
                                                <hr></hr>
                                                <div className={styles.additionsToProductCounter}>
                                                    {AdditionBtnLIst.map((value, index) => {
                                                        const addition = value as keyof AdditionsProps["additions"]

                                                        const additionName = addition.charAt(0).toUpperCase() + addition.slice(1)
                                                        return (
                                                            <div key={index} className={styles.additionsToProductContainer}>
                                                                <div className={styles.btnContainer}>
                                                                    <button disabled={
                                                                        productData["additions"][addition] === 0
                                                                    } onClick={() => setAdditionData({ type: "decrement", field: "additions", subField: addition, price: 2 })}>
                                                                        <CircleMinus size={32} />
                                                                    </button>
                                                                    <span>{productData["additions"][addition]}</span>
                                                                    <button onClick={() => setAdditionData({ type: "increment", field: "additions", subField: addition, price: 2 })}
                                                                    >
                                                                        <CirclePlus size={32} />
                                                                    </button>
                                                                </div>
                                                                <div className={styles.additionInformation}>
                                                                    <span>{additionName}: 2 </span>
                                                                </div>
                                                            </div>
                                                        )
                                                    })}
                                                    <p>
                                                        The y value is an internal MotionValue that represents the distance to the top most position of the sheet when it is fully open. So for example the y value is zero when the sheet is completely open.

                                                        Similarly to the snapTo method the y value can be accessed via a ref.

                                                        The y value can be useful for certain situtation eg. when you want to combine snap points with scrollable sheet content and ensure that the content stays properly scrollable in any snap point. Below you can see a simplified example of this situation and for a more detailed example take a look at the ScrollableSnapPoints component in the example app.
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Sheet.Scroller>
                        <PopUpFooter />
                    </Sheet.Content>
                </Sheet.Container>
            </Sheet>
        </>
    )
}
