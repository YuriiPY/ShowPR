'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import Image from 'next/image'
import styles from './Paydesk.module.scss'

import clsx from 'clsx'
import { useTranslations } from 'next-intl'
import { DeliveryForm } from './Forms/DeliveryForm/DeliveryForm'
import { PaymentForm } from './Forms/PaymentForm/PaymentForm'
import { UserDataForm } from './Forms/UserDataForm/UserDataForm'

type ProductProps = {
    tableName: string
    itemId: number
    name: string
    img: string
    description: string
    price: number
    type: "by weight" | "by portion"
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

type BasketProps = {
    [key: string]: { product: ProductProps, productData: AdditionsProps }
}

type Addition = {
    [key: string]: number | null
}

interface Check {
    products: {
        [key: string]: number
    },
    amount: number
}

export default function ProductsCheck() {

    const [check, setCheck] = useState<Check>({
        products: {},
        amount: 0
    })

    // const [formData, setFormData] = useState(
    //     {
    //         fullName: "",
    //         email: "",
    //         phone: "",
    //         verify: false,
    //         street: "",
    //         home: "",
    //         homeNumber: "",
    //         paymentMethod: ""
    //     }
    // )

    const [currentForm, setCurrentForm] = useState(1)

    const handleFormStep = useCallback((step: "next" | "back") => {
        if (step === "next") {
            setCurrentForm((prev) => prev + 1)
        } else if (step === "back") {
            setCurrentForm((prev) => prev - 1)
        }
    }, [])

    const t = useTranslations("paydesk.Check")

    const paydeskRef = useRef<HTMLDivElement | null>(null)

    const statusBarRef = useRef<HTMLDivElement | null>(null)

    useEffect(() => {
        if (statusBarRef.current) {
            console.log(currentForm, statusBarRef.current.style.width,)
            statusBarRef.current.style.width = ((currentForm - 1) / 3) * 100 + "%"
            console.log(statusBarRef.current.style.width,)

        }
    }, [currentForm])

    useEffect(() => {
        const basket: BasketProps = JSON.parse(localStorage.getItem("basket") || "{}")

        const productsData = Object.entries(basket).reduce((acc, [productName, productInfo]) => {
            acc[productName] = {
                tableName: productInfo.product.tableName,
                productId: productInfo.product.itemId,
                quantity: productInfo.productData.quantity,
                weight: productInfo.productData.weight,
                additions: { ...productInfo.productData.additions }
            }
            return acc
        }, {} as Record<string, { tableName: string, productId: number, quantity: number, weight: number, additions: Addition }>)

        const url = process.env.NEXT_PUBLIC_BACKEND_API_URL
        const apiUrl = new URL("order/get_amount", url).href

        const fetchData = async () => {
            try {
                const request = new Request(apiUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(productsData)
                })

                const response = await fetch(request)

                if (!response.ok) {
                    throw new Error(`Failed to fetch data from ${apiUrl}`)
                }

                const data = await response.json()

                setCheck({ products: data["products"], amount: data["totalAmount"] })


            } catch (error) {
                console.log(error)
            } finally {
            }
        }

        fetchData()
    }, [])

    useEffect(() => {

        console.log("Current index form", currentForm)
        paydeskRef.current?.scrollIntoView({ behavior: "smooth", block: "center" })
    }, [currentForm])


    // const handleSubmit = async (e: React.FormEvent) => {
    //     e.preventDefault()
    //     const personalPhone = firstDataForm.phone
    //     try {
    //         const response = await fetch("/order/verify_phone", {
    //             method: "POST",
    //             headers: {
    //                 "Content-Type": "application/json"
    //             },
    //             body: JSON.stringify(personalPhone)
    //         })

    //         if (!response.ok) {
    //             throw new Error("Failed to send data")

    //             const result = await response.json()
    //         }

    //     } catch (error) {

    //     }
    // }

    const Check = useMemo(() => (
        Object.entries(check.products).map(([productName, productAmount], index) => {
            return (
                <li key={index} className={styles.singleProduct}>
                    <div className={styles.singleProductContainer}>
                        <span className={styles.productName}>
                            {productName}
                        </span>
                        {productAmount ? (
                            <span className={styles.productAmount}>
                                {productAmount}
                            </span>
                        ) : (
                            <span className={styles.notAvailable}>
                                Is not available
                            </span>
                        )}
                    </div>
                </li>
            )
        })
    ), [check])

    return (
        <div className={styles.paydesk}>
            <div className={styles.container}>
                <div className={styles.checkTable}>
                    <div className={styles.dynamicColumn}>
                        <div className={styles.containerForm}>
                            <div
                                className={styles.formArea}
                                ref={paydeskRef}
                            >
                                {
                                    (currentForm === 1 || currentForm === 2) && <UserDataForm
                                        handleFormStep={handleFormStep} />
                                }
                                {
                                    currentForm === 3 && <DeliveryForm checkAmount={check.amount} handleFormStep={handleFormStep} />
                                }
                                {
                                    currentForm === 4 && <PaymentForm handleFormStep={handleFormStep} />
                                }
                            </div>
                        </div>
                    </div>
                    <div className={styles.productsCheckColumn}>
                        <div className={styles.productCheckArea}>
                            <div className={styles.productCheckTitle}>
                                <span>{t("title")}</span>
                                <Image src={'/icons/under-line.png'} alt={''} width={200} height={10} />
                            </div>
                            <ol type='1' className={styles.productsList}>
                                {Check}
                            </ol>
                            <div className={styles.totalAmount}>
                                <span>{t("additionalText")}</span>
                                <span className={styles.amount}>{check.amount}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className={styles.statusForm}>
                <div className={styles.statusContainer}>
                    <div className={styles.status}>
                        <div ref={statusBarRef} className={clsx(styles.statusBar)}></div>

                        <div className={styles.statusPoints}>
                            <div className={styles.statusPointContainer}>
                                <div className={clsx(styles.statusPoint,
                                    {
                                        [styles.active]: currentForm > 0
                                    }
                                )}>
                                    <span>1</span>
                                </div>
                            </div>
                            <div className={styles.statusPointContainer}>
                                <div className={clsx(styles.statusPoint,
                                    {
                                        [styles.active]: currentForm > 1
                                    }
                                )}>
                                    <span>2</span>
                                </div>
                            </div>
                            <div className={styles.statusPointContainer}>
                                <div className={clsx(styles.statusPoint,
                                    {
                                        [styles.active]: currentForm > 2
                                    }
                                )}>
                                    <span>3</span>
                                </div>
                            </div>
                            <div className={styles.statusPointContainer}>
                                <div className={clsx(styles.statusPoint,
                                    {
                                        [styles.active]: currentForm > 3
                                    }
                                )}>
                                    <span>4</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div >
    )
}
