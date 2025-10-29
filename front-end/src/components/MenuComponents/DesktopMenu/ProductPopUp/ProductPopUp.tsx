import { AnimatePresence, motion } from 'framer-motion'
import Image from 'next/image'
import { useCallback, useEffect, useReducer, useRef, useState } from 'react'
import 'react-spring-bottom-sheet/dist/style.css'

import clsx from 'clsx'
import { CircleMinus, CirclePlus, CircleX } from 'lucide-react'
import { useTranslations } from 'next-intl'
import styles from './ProductPopUp.module.scss'

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
    closePopUp: () => void,
    isPopUpOpen: boolean
}

type AdditionsProps = {
    amount: number
    quantity: number
    weight: number
    additions: {
        cutlery: number
        onion: number
        cream: number
    }
}

type NestedField = {
    field: "additions"
    subField: keyof AdditionsProps["additions"]
}

type PopUpDataAction =
    | { type: "increment" | "decrement", field: keyof AdditionsProps; price: number }
    | ({ type: "increment" | "decrement", price: number } & NestedField)
    | { type: "weight_update", value: number, price: number }
    | { type: "bulk-update", field: Partial<AdditionsProps> }

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
                const newWeightPrice = newWeight * action.price
                const additionAmount = state.amount - (state.weight * action.price)
                return {
                    ...state,
                    weight: newWeight,
                    amount: newWeightPrice + additionAmount
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
        case "weight_update":
            return {
                ...state,
                weight: action.value,
                amount: (state.amount - (state.weight * action.price)) + (action.value * action.price)
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

export default function ProductPopUp({ product, closePopUp, isPopUpOpen }: PopUpProps) {

    const [productData, setAdditionData] = useReducer(reducer, {
        amount: product.type === "by portion"
            ? product.price
            : product.price * 100,
        quantity: 1,
        weight: 100,
        additions: {
            cutlery: 0,
            onion: 0,
            cream: 0
        }
    })

    const [isButtonHovered, setIsButtonHovered] = useState<boolean>(false)

    const productCardDialog = useRef<HTMLDialogElement | null>(null)

    const handleClosePopUp = useCallback(() => {
        closePopUp()
        document.body.style.overflow = ''
    }, [closePopUp])


    useEffect(() => {
        const cardDialog = productCardDialog.current

        if (!cardDialog) return

        if (isPopUpOpen) {
            document.body.style.overflow = 'hidden'
            cardDialog.showModal()
        }
        const closePopUp = (e: Event) => {
            e.preventDefault()
            handleClosePopUp()
        }

        cardDialog.addEventListener('cancel', closePopUp)

        return () => cardDialog.addEventListener('cancel', closePopUp)
    }, [handleClosePopUp, isPopUpOpen])


    const t = useTranslations("TextForScreenReader")


    if (!product) return null


    return (

        <AnimatePresence
            onExitComplete={() => {
                productCardDialog.current?.close()
            }}
        >
            {isPopUpOpen && (
                <dialog ref={productCardDialog}
                    onClick={(e: React.MouseEvent<HTMLDialogElement>) => {
                        if (e.target === e.currentTarget) handleClosePopUp()
                    }}
                    className={styles.productCardPopUp}
                >
                    <motion.div
                        className={styles.popUpContainer}
                        initial={{ opacity: 0, y: 100 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 100 }}
                        transition={{ duration: .3, ease: "easeInOut" }}
                    >
                        <button
                            type='button'
                            aria-label={t("buttons.closePopUpButton")}
                            className={styles.dialogCloseBtn}
                            onClick={handleClosePopUp}
                        >
                            <CircleX size={30} />
                        </button>
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
                                                    <button
                                                        type='button'
                                                        aria-label={t("menuText.popUpTexts.reduceProductButton")}
                                                        disabled={
                                                            productData.quantity === 0
                                                        }
                                                        onClick={() => setAdditionData({ type: "decrement", field: "quantity", price: product.price })}>
                                                        <CircleMinus size={32} />
                                                    </button>
                                                    <span
                                                        aria-label={t("menuText.popUpTexts.productCount")}
                                                    >{productData.quantity}</span>
                                                    <button
                                                        type='button'
                                                        aria-label={t("menuText.popUpTexts.reduceProductButton")}
                                                        onClick={() => setAdditionData({ type: "increment", field: "quantity", price: product.price })}
                                                    >
                                                        <CirclePlus size={32} />
                                                    </button>
                                                </div> :
                                                product.type === "by weight" ?
                                                    <div className={styles.btnContainer}>
                                                        <button disabled={
                                                            productData.weight === 0
                                                        } onClick={() => setAdditionData({ type: "decrement", field: "weight", price: product.price })}>
                                                            <CircleMinus size={32} />
                                                        </button>
                                                        <span>{productData.weight}</span>
                                                        <button onClick={() => setAdditionData({ type: "increment", field: "weight", price: product.price })}
                                                        >
                                                            <CirclePlus size={32} />
                                                        </button>
                                                    </div> :
                                                    null
                                            }
                                            <div className={styles.additionInformation}>
                                                <span className={clsx(
                                                    styles.popUpProductPrice,

                                                    product.type === "by portion" && styles.byPortionPrice,

                                                    product.type === "by weight" && styles.byWeightPrice

                                                )}
                                                >{product.price}</span>
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
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className={styles.footerPopUp}>
                            <div className={styles.footerContainer}>
                                <div className={styles.infoAmount}>
                                    <span>Total amount: {productData.amount} </span>
                                </div>
                                <div className={styles.addBtnContainer}>
                                    <button
                                        className={styles.addToBasketBtn}
                                        disabled={!product.status}
                                        onMouseEnter={() => setIsButtonHovered(true)}
                                        onMouseLeave={() => setIsButtonHovered(false)}
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
                                            handleClosePopUp()
                                        }}
                                    >
                                        <span>
                                            Add to basket
                                        </span>
                                    </button>
                                    <AnimatePresence>
                                        {(!product.status && isButtonHovered) &&
                                            <motion.div
                                                className={styles.hintContainer}
                                                initial={{ opacity: 0, y: -40 }}
                                                animate={{ opacity: .7, y: -80 }}
                                                exit={{ opacity: 0, y: -40 }}
                                                transition={{ duration: .3, ease: "linear" }}
                                            >
                                                <p>
                                                    Store is closed!
                                                </p>
                                            </motion.div>
                                        }
                                    </AnimatePresence>

                                </div>
                            </div>
                        </div>
                    </motion.div>
                </dialog >
            )}
        </AnimatePresence>

    )
}
