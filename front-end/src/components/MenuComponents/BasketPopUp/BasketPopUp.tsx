'use client'

import { CircleMinus, CirclePlus, CircleX, Trash2 } from 'lucide-react'
import { useCallback, useEffect, useMemo, useReducer, useRef, useState } from 'react'

import BasketIcon from '@/components/svgIcons/basketIcon'
import DumplingIcon from '@/components/svgIcons/dumplingIcon'
import { useQuery } from '@tanstack/react-query'
import { AnimatePresence, motion, useAnimation } from 'framer-motion'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import React from 'react'
import { Sheet } from 'react-modal-sheet'
import styles from './BasketPopUp.module.scss'
import mobileStyles from './MobileBasketPopUp.module.scss'


type StoreStatus = {
    isOpen: boolean
    until: string
    changedAt: string
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

type Product = {
    name: string
    img: string
    description: string
    price: number
    type: "by portion" | "by weight"
}

type BasketState = {
    [key: string]: { product: Product, productData: AdditionsProps }
}

type BasketAction =
    | { type: "increment" | "decrement", name: string, field: "addition", subField: keyof AdditionsProps["additions"] }
    | { type: "increment" | "decrement", name: string, field: keyof AdditionsProps }
    | { type: "update_local_storage" }
    | { type: "update_basket", payload: BasketState }
    | { type: "delete_product", name: string }
    | { type: "clear_basket" }

const basketReducer = (state: BasketState, action: BasketAction): BasketState => {
    switch (action.type) {
        case "increment":
            if (action.field === "addition" && "subField" in action) {
                return {
                    ...state,
                    [action.name]: {
                        ...state[action.name],
                        productData: {
                            ...state[action.name].productData,
                            additions: {
                                ...state[action.name].productData.additions,
                                [action.subField]: state[action.name].productData.additions[action.subField] + 1
                            },
                            amount: state[action.name].productData.amount + 2
                        }
                    }
                }
            } else if (action.field === 'quantity') {
                const news = {
                    ...state,
                    [action.name]: {
                        ...state[action.name],
                        productData: {
                            ...state[action.name].productData,
                            [action.field]: Math.max(0, (state[action.name].productData[action.field] as number) + 1),
                            amount: state[action.name].productData.amount + state[action.name].product.price
                        }
                    }
                }
                console.log(news[action.name].productData)
                return news
            }
            else if (action.field === "weight") {
                const newWeight = Math.max(0, state[action.name].productData.weight + 100)
                const newWeightPrice = newWeight * state[action.name].product.price
                const additionAmount = state[action.name].productData.amount - (state[action.name].productData.weight * state[action.name].product.price)
                return {
                    ...state,
                    [action.name]: {
                        ...state[action.name],
                        productData: {
                            ...state[action.name].productData,
                            weight: newWeight,
                            amount: newWeightPrice + additionAmount
                        }
                    }
                }
            }
        case "decrement":
            if (action.field === "addition" && "subField" in action) {
                return {
                    ...state,
                    [action.name]: {
                        ...state[action.name],
                        productData: {
                            ...state[action.name].productData,
                            additions: {
                                ...state[action.name].productData.additions,
                                [action.subField]: state[action.name].productData.additions[action.subField] - 1
                            },
                            amount: state[action.name].productData.amount - 2
                        }
                    }
                }
            } else if (action.field === 'quantity') {
                return {
                    ...state,
                    [action.name]: {
                        ...state[action.name],
                        productData: {
                            ...state[action.name].productData,
                            [action.field]: Math.max(0, (state[action.name].productData[action.field] as number) - 1),
                            amount: state[action.name].productData.amount - state[action.name].product.price
                        }
                    }
                }
            }
            else if (action.field === "weight") {
                const newWeight = Math.max(0, state[action.name].productData.weight - 100)
                const newWeightPrice = newWeight * state[action.name].product.price
                const additionAmount = state[action.name].productData.amount - (state[action.name].productData.weight * state[action.name].product.price)
                return {
                    ...state,
                    [action.name]: {
                        ...state[action.name],
                        productData: {
                            ...state[action.name].productData,
                            weight: newWeight,
                            amount: newWeightPrice + additionAmount
                        }
                    }
                }
            }

        case "update_local_storage":
            localStorage.setItem("basket", JSON.stringify(state))
            window.dispatchEvent(new Event("basketUpdated"))
            return state

        case "update_basket":
            return action.payload

        case "delete_product":
            const newState = { ...state }
            delete newState[action.name]
            localStorage.setItem("basket", JSON.stringify(newState))
            return newState

        case "clear_basket":
            localStorage.removeItem("basket")
            return {}

        default:
            return state
    }
}


const BasketPopUp = React.memo(() => {

    const [isBasketOpen, setIsBasketOpen] = useState(false)

    const [isBasketIconOpen, setIsBasketIconOpen] = useState(false)

    const [isBasketButtonHovered, setIsBasketButtonHovered] = useState(false)

    const [basketFullInfo, basketDispatcher] = useReducer<React.Reducer<BasketState, BasketAction>>(basketReducer, {})

    const [windowWidth, setWindowWidth] = useState<number | null>(null)

    const basketDialog = useRef<HTMLDialogElement | null>(null)

    const animation = useAnimation()

    const router = useRouter()

    const [itemCount, changes, totalAmount] = useMemo(() => {
        const count = Object.keys(basketFullInfo).length
        let change: number = 0

        Object.entries(basketFullInfo).forEach(([, { productData }]) => {
            change += productData.quantity + count
        })

        const totalAmount = Object.values(basketFullInfo).reduce((sum, item) => sum + item.productData.amount, 0)

        console.log(count, change, totalAmount)

        return [count, change, totalAmount]
    }, [basketFullInfo])

    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL
    const storeStatusUrl = new URL("store/status", backendUrl).href

    const { data: storeStatus } = useQuery<StoreStatus>({
        queryKey: ["storeStatus"],
        queryFn: async () => {
            const res = await fetch(storeStatusUrl)
            if (!res.ok) throw new Error(`Failed to fetch ${storeStatusUrl}`)
            return res.json()
        }
    })


    useEffect(() => {
        animation.start({
            x: [-120, -80, -40, -25, 0],
            y: [-120, -80, -45, -25, 0],
            rotate: [45, 90, 180, 360],
            transition: {
                duration: 1.5,
                ease: "linear",
            },
        })
    }, [animation, changes])

    useEffect(() => {

        const handleUpdated = () => {
            const basket = JSON.parse(localStorage.getItem("basket") || "{}")
            basketDispatcher({ type: "update_basket", payload: basket })
            console.log("I`M UPDATING BASKET", "\nBASKET FROM LOCAL_STORAGE", basket)
        }

        handleUpdated()

        window.addEventListener("basketUpdated", handleUpdated)
        return () => {
            window.removeEventListener("basketUpdated", handleUpdated)
        }
    }, [])

    useEffect(() => {
        if (typeof window !== 'undefined') setWindowWidth(window.innerWidth)
    }, [])


    useEffect(() => {
        setIsBasketIconOpen(true)
        const timer = setTimeout(() => {
            setIsBasketIconOpen(false)
        }, 2500)

        return () => clearTimeout(timer)
    }, [changes])


    useEffect(() => {
        const basketD = basketDialog.current

        if (!basketD) return

        if (isBasketOpen && windowWidth !== null && windowWidth >= 620) {
            document.body.style.overflow = 'hidden'
            basketD.showModal()
        } else if (!isBasketOpen && windowWidth !== null && windowWidth >= 620) {
            document.body.style.overflow = ''
        }

        const closeDialogPopUp = (e: Event) => {
            e.preventDefault()
            setIsBasketOpen(false)
        }

        basketD.addEventListener('cancel', closeDialogPopUp)
        return () => {
            basketD.removeEventListener('cancel', closeDialogPopUp)
        }
    }, [isBasketOpen, windowWidth])


    const handleCloseMobilePopUp = useCallback(() => {
        setIsBasketOpen(false)
    }, [])


    const MobileProducts = ({ basketFullInfo, basketDispatcher }: { basketFullInfo: BasketState, basketDispatcher: React.Dispatch<BasketAction> }) => (
        Object.entries(basketFullInfo).map(([productName, productInfo], index) => (
            <div key={index} className={mobileStyles.singleBasketProduct}>
                <div className={mobileStyles.mainInformation}>
                    <div className={mobileStyles.imgSection}>
                        <div className={mobileStyles.imgContainer}>ʼ
                            <Image src={productInfo.product.img} alt={''} width={100} height={100} objectFit='fill' />
                        </div>
                    </div>
                    <div className={mobileStyles.nameContainer}>
                        <span>{productName}</span>
                    </div>
                    <div className={mobileStyles.productCounter}>
                        <div className={mobileStyles.btnCounter}>
                            {productInfo.product.type === "by weight" ? (
                                <>
                                    <button disabled={productInfo.productData.weight === 0}
                                        onClick={() => {
                                            if (productInfo.productData.weight
                                                === 100) {
                                                basketDispatcher({
                                                    type: "delete_product",
                                                    name: productName
                                                })
                                            } else {
                                                basketDispatcher({
                                                    type: "decrement",
                                                    name: productName,
                                                    field: "weight"
                                                })
                                            }
                                        }}
                                    >
                                        <CircleMinus size={32} />
                                    </button>
                                    <span>{productInfo.productData.weight}</span>
                                    <button
                                        onClick={() => {
                                            basketDispatcher({
                                                type: "increment",
                                                name: productName,
                                                field: "weight"
                                            })
                                        }}
                                    >
                                        <CirclePlus size={32} />
                                    </button>
                                </>
                            ) : productInfo.product.type === "by portion" && (
                                <>
                                    <button disabled={productInfo.productData.quantity === 0}
                                        onClick={() => {
                                            if (productInfo.productData.quantity === 1) {
                                                basketDispatcher({
                                                    type: "delete_product",
                                                    name: productName
                                                })
                                            } else {
                                                basketDispatcher({
                                                    type: "decrement",
                                                    name: productName,
                                                    field: "quantity"
                                                })
                                            }
                                        }}
                                    >
                                        <CircleMinus size={32} />
                                    </button>
                                    <span>{productInfo.productData.quantity}</span>
                                    <button
                                        onClick={() => {
                                            basketDispatcher({
                                                type: "increment",
                                                name: productName,
                                                field: "quantity"
                                            })
                                        }}
                                    >
                                        <CirclePlus size={32} />
                                    </button>
                                </>
                            )
                            }
                        </div>
                    </div>
                    <div className={mobileStyles.sumContainer}>
                        <div className={mobileStyles.productAmount}>
                            <span>{productInfo.productData.amount}</span>
                        </div>
                    </div>
                </div>
                <div className={mobileStyles.additionalInformation}>
                    {
                        Object.entries(productInfo.productData.additions).map(([additionName, additionValue], index) => {
                            const additionFullname = additionName.charAt(0).toUpperCase() + additionName.slice(1)

                            return (
                                <div key={index} className={mobileStyles.additionContainer}>
                                    <div className={mobileStyles.additionBtnContainer}>
                                        <button disabled={additionValue === 0}
                                            onClick={() => {
                                                basketDispatcher({
                                                    type: "decrement",
                                                    name: productName,
                                                    field: "addition",
                                                    subField: additionName as keyof AdditionsProps["additions"]

                                                })
                                            }}
                                        >
                                            <CircleMinus size={32} />
                                        </button>
                                        <span>{additionValue}</span>
                                        <button
                                            onClick={() => {
                                                basketDispatcher({
                                                    type: "increment",
                                                    name: productName,
                                                    field: "addition",
                                                    subField: additionName as keyof AdditionsProps["additions"]

                                                })
                                            }}
                                        >
                                            <CirclePlus size={32} />
                                        </button>
                                    </div>
                                    <div className={mobileStyles.additionPriceInform}>
                                        <span>{additionFullname}: 2</span>
                                    </div>
                                </div>
                            )
                        })
                    }
                </div>
            </div>
        ))
    )

    const Products = ({ basketFullInfo, basketDispatcher }: { basketFullInfo: BasketState, basketDispatcher: React.Dispatch<BasketAction> }) => (
        Object.entries(basketFullInfo).map(([productName, productInfo], index) => (
            <div key={index} className={styles.singleBasketProduct}>
                <div className={styles.mainInformation}>
                    <div className={styles.imgSection}>
                        <div className={styles.imgContainer}>ʼ
                            <Image src={productInfo.product.img} alt={''} width={100} height={100} objectFit='fill' />
                        </div>
                    </div>
                    <div className={styles.nameContainer}>
                        <span>{productName}</span>
                    </div>
                    <div className={styles.productCounter}>
                        <div className={styles.btnCounter}>
                            {productInfo.product.type === "by weight" ? (
                                <>
                                    <button disabled={productInfo.productData.weight === 0}
                                        onClick={() => {
                                            if (productInfo.productData.weight
                                                === 100) {
                                                basketDispatcher({
                                                    type: "delete_product",
                                                    name: productName
                                                })
                                            } else {
                                                basketDispatcher({
                                                    type: "decrement",
                                                    name: productName,
                                                    field: "weight"
                                                })
                                            }
                                        }}
                                    >
                                        <CircleMinus size={32} />
                                    </button>
                                    <span>{productInfo.productData.weight}</span>
                                    <button
                                        onClick={() => {
                                            basketDispatcher({
                                                type: "increment",
                                                name: productName,
                                                field: "weight"
                                            })
                                        }}
                                    >
                                        <CirclePlus size={32} />
                                    </button>
                                </>
                            ) : productInfo.product.type === "by portion" && (
                                <>
                                    <button disabled={productInfo.productData.quantity === 0}
                                        onClick={() => {
                                            if (productInfo.productData.quantity === 1) {
                                                basketDispatcher({
                                                    type: "delete_product",
                                                    name: productName
                                                })
                                            } else {
                                                basketDispatcher({
                                                    type: "decrement",
                                                    name: productName,
                                                    field: "quantity"
                                                })
                                            }
                                        }}
                                    >
                                        <CircleMinus size={32} />
                                    </button>
                                    <span>{productInfo.productData.quantity}</span>
                                    <button
                                        onClick={() => {
                                            basketDispatcher({
                                                type: "increment",
                                                name: productName,
                                                field: "quantity"
                                            })
                                        }}
                                    >
                                        <CirclePlus size={32} />
                                    </button>
                                </>
                            )
                            }
                        </div>
                    </div>
                    <div className={styles.sumContainer}>
                        <div className={styles.productAmount}>
                            <span>{productInfo.productData.amount}</span>
                        </div>
                    </div>
                </div>
                <div className={styles.additionalInformation}>
                    {
                        Object.entries(productInfo.productData.additions).map(([additionName, additionValue], index) => {
                            const additionFullname = additionName.charAt(0).toUpperCase() + additionName.slice(1)

                            return (
                                <div key={index} className={styles.additionContainer}>
                                    <div className={styles.additionBtnContainer}>
                                        <button disabled={additionValue === 0}
                                            onClick={() => {
                                                basketDispatcher({
                                                    type: "decrement",
                                                    name: productName,
                                                    field: "addition",
                                                    subField: additionName as keyof AdditionsProps["additions"]

                                                })
                                            }}
                                        >
                                            <CircleMinus size={32} />
                                        </button>
                                        <span>{additionValue}</span>
                                        <button
                                            onClick={() => {
                                                basketDispatcher({
                                                    type: "increment",
                                                    name: productName,
                                                    field: "addition",
                                                    subField: additionName as keyof AdditionsProps["additions"]

                                                })
                                            }}
                                        >
                                            <CirclePlus size={32} />
                                        </button>
                                    </div>
                                    <div className={styles.additionPriceInform}>
                                        <span>{additionFullname}: 2</span>
                                    </div>
                                </div>
                            )
                        })
                    }
                </div>
            </div>
        ))
    )

    // Products.displayName = 'Products'

    // const MobileBasketHeader = () => (
    //     <div className={mobileStyles.mobileBasketHeader}>
    //         <div className={mobileStyles.basketTitle}>
    //             <span>Basket:</span>
    //         </div>
    //         <div className={mobileStyles.basketClearBtn}>
    //             {/* <Button
    //                 type={'elevated'}
    //                 buttonName={'Clear basket'}
    //                 buttonHover='changeColor'
    //                 onClick={() => {
    //                     if (confirm("Do you want to delete all products?")) {
    //                         basketDispatcher({ type: "clear_basket" })
    //                     } else {
    //                         return
    //                     }
    //                 }} /> */}
    //         </div>
    //     </div >

    // )

    const MobileBasketFooter = () => (
        <div className={mobileStyles.mobileBasketFooter}>
            <div className={mobileStyles.totalAmount}>

                <button
                    className={mobileStyles.clearBasketButton}
                    onClick={() => {
                        if (confirm("Do you want to delete all products?")) {
                            basketDispatcher({ type: "clear_basket" })
                        } else {
                            return
                        }
                    }}
                >
                    <span>
                        <Trash2 size={30} />
                    </span>
                </button>

                <button
                    disabled={!storeStatus?.isOpen}
                    className={mobileStyles.basketBuyButton}
                    onClick={() => {
                        router.push("/menu/paydesk")
                    }}>
                    <span>Buy: {Object.values(basketFullInfo).reduce((sum, item) => sum + item.productData.amount, 0)}</span>
                </button>
            </div>
        </div>
    )


    return (
        <>
            <div className={styles.basket}>
                <div className={styles.basketBtnContainer}>
                    <div className={styles.basketOverlay} />
                    <button
                        className={styles.basketBtn}
                        onClick={() => {
                            setIsBasketOpen(true)
                        }}
                        onMouseEnter={() => setIsBasketButtonHovered(true)}
                        onMouseLeave={() => setIsBasketButtonHovered(false)}
                    >
                        {windowWidth != null && windowWidth > 768 ? (
                            <>
                                <div className={styles.basketAmountIconContainer}>
                                    <span className={styles.basketAmountIcon}>
                                        {totalAmount}
                                    </span>
                                </div>
                                {/* <AnimatePresence>
                                    {(isBasketButtonHovered || isBasketOpen)
                                        &&
                                        <motion.div
                                            className={styles.basketAmountIconContainer}
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            exit={{ opacity: 0 }}
                                            transition={{
                                                duration: .5,
                                                ease: "linear"
                                            }}
                                        >
                                            <motion.span
                                                className={styles.basketAmountIcon}
                                                initial={{ opacity: 0 }}
                                                animate={{ opacity: 1 }}
                                                exit={{ opacity: 0 }}
                                                transition={{
                                                    duration: .2,
                                                    ease: "linear"
                                                }}
                                            >
                                                {totalAmount}
                                            </motion.span>
                                        </motion.div>
                                    }
                                </AnimatePresence> */}
                                <AnimatePresence>
                                    {(isBasketButtonHovered || isBasketOpen)
                                        &&
                                        <motion.div
                                            className={styles.basketCountIconContainer}
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            exit={{ opacity: 0 }}
                                            transition={{
                                                duration: .5,
                                                ease: "linear"
                                            }}
                                        >
                                            <motion.span
                                                className={styles.basketCountIcon}
                                                initial={{ opacity: 0 }}
                                                animate={{ opacity: 1 }}
                                                exit={{ opacity: 0 }}
                                                transition={{
                                                    duration: .2,
                                                    ease: "linear"
                                                }}
                                            >
                                                {itemCount}
                                            </motion.span>
                                        </motion.div>
                                    }
                                </AnimatePresence>
                            </>
                        ) :
                            <div className={styles.mobileBasketAmountIconContainer}>
                                <span className={styles.mobileBasketAmountIcon}>{totalAmount}</span>
                            </div>
                        }
                        <motion.div
                            className={styles.basketContentContainer}
                            animate={animation}
                        >
                            {itemCount != 0 && <DumplingIcon size={"90%"} />}
                        </motion.div>

                        <div className={styles.basketIconContainer}>
                            <BasketIcon size={65} isOpen={isBasketIconOpen} />
                        </div>
                    </button>
                </div>
            </div >
            <div>
                {windowWidth !== null && windowWidth <= 768 ? (
                    <Sheet
                        isOpen={isBasketOpen}
                        onClose={handleCloseMobilePopUp}
                        snapPoints={[0.8]}
                        dragCloseThreshold={0.3}
                    >
                        <Sheet.Container>
                            <Sheet.Header>

                            </Sheet.Header>
                            <Sheet.Header>
                                {!storeStatus?.isOpen &&
                                    <div className={mobileStyles.storeInformation}>
                                        <p className={mobileStyles.information}>
                                            {storeStatus?.until
                                                ? `Store is closed until ${storeStatus.until}`
                                                : 'Store status closed before open'}
                                        </p>
                                    </div>
                                }
                            </Sheet.Header>
                            <Sheet.Content>
                                {/* <MobileBasketHeader /> */}
                                <Sheet.Scroller>

                                    <div className={mobileStyles.mobileBasketContainer}>
                                        <div className={mobileStyles.mainContainer}>
                                            <div className={mobileStyles.mainArea}>
                                                <div className={mobileStyles.scrollContainer}>
                                                    <div className={mobileStyles.productsArea}>
                                                        <MobileProducts basketFullInfo={basketFullInfo} basketDispatcher={basketDispatcher} />
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </Sheet.Scroller>
                                <MobileBasketFooter />
                            </Sheet.Content>
                        </Sheet.Container>
                    </Sheet>
                ) : <AnimatePresence >
                    {
                        isBasketOpen && (
                            <dialog ref={basketDialog}
                                className={styles.basketDialog}
                                onClick={(e: React.MouseEvent<HTMLDialogElement>) => {
                                    if (e.target === e.currentTarget) {
                                        setIsBasketOpen(false)
                                    }
                                }}
                            >
                                <motion.div
                                    className={styles.basketContainer}
                                    initial={{ opacity: 0, y: 100 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: 100 }}
                                    transition={{ duration: .3, ease: "easeInOut" }}
                                    onAnimationComplete={(definition) => {
                                        if (definition === "exit") { basketDialog.current?.close() }
                                    }}
                                >
                                    <button className={styles.dialogCloseBtn} onClick={() => setIsBasketOpen(false)}>
                                        <CircleX size={30} />
                                    </button>
                                    <div className={styles.mainContainer}>
                                        <div className={styles.mainArea}>
                                            {/* <div className={styles.basketHeader}>
                                        <div className={styles.basketTitle}>
                                            <span>Basket:</span>
                                        </div>
                                        <div className={styles.basketClearBtn}>
                                            <Button
                                                type={'elevated'}
                                                buttonName={'Clear basket'}
                                                buttonHover='changeColor'
                                                onClick={() => {
                                                    if (confirm("Do you want to delete all products?")) {
                                                        basketDispatcher({ type: "clear_basket" })
                                                    } else {
                                                        return
                                                    }
                                                }} />
                                        </div>
                                    </div> */}
                                            <div className={styles.scrollContainer}>
                                                {!storeStatus?.isOpen &&
                                                    <div className={styles.storeInformation}>
                                                        <p className={styles.information}>
                                                            {storeStatus?.until
                                                                ? `Store is closed until ${storeStatus.until}`
                                                                : 'Store status closed before open'}
                                                        </p>
                                                    </div>
                                                }
                                                <div className={styles.productsArea}>
                                                    <Products basketFullInfo={basketFullInfo} basketDispatcher={basketDispatcher} />
                                                </div>
                                            </div>
                                            <div className={styles.basketFooter}>
                                                <div className={styles.totalAmount}>
                                                    <button
                                                        className={styles.clearBasketButton}
                                                        onClick={() => {
                                                            if (confirm("Do you want to delete all products?")) {
                                                                basketDispatcher({ type: "clear_basket" })
                                                            } else {
                                                                return
                                                            }
                                                        }}
                                                    >
                                                        <span>
                                                            <Trash2 size={30} />
                                                        </span>
                                                    </button>

                                                    <button
                                                        disabled={!storeStatus?.isOpen}
                                                        className={styles.basketBuyButton}
                                                        onClick={() => {
                                                            router.push("/menu/paydesk")
                                                            setIsBasketOpen(false)
                                                        }}>
                                                        <span>Buy: {Object.values(basketFullInfo).reduce((sum, item) => sum + item.productData.amount, 0)}</span>
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </motion.div>
                            </dialog>
                        )
                    }
                </AnimatePresence>
                }



            </div>
        </>
    )
})


BasketPopUp.displayName = 'BasketPopUp'

export default BasketPopUp

