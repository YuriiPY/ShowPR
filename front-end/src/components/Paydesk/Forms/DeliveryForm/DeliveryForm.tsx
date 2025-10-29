import Cookies from "js-cookie"
import Image from 'next/image'
import React, { useCallback, useEffect, useReducer, useState } from 'react'

import clsx from 'clsx'


import { motion } from 'framer-motion'
import { useTranslations } from 'next-intl'
import TimePeakier from '../../../TimePeakier/TimePeakier'
import styles from './DeliveryForm.module.scss'




interface locationProps {
    street: ""
    home: "" | null
}

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

type Addition = {
    [key: string]: number | null
}

type BasketProps = {
    [key: string]: { product: ProductProps, productData: AdditionsProps }
}


type Timer = {
    hours: number,
    minutes: number
}

type TimerAction =
    | { type: "increment" | "decrement", field: "hours" }
    | { type: "increment" | "decrement", field: "minutes" }
    | { type: "update", field: Timer }

const Dispatcher = (state: Timer, action: TimerAction): Timer => {
    switch (action.field) {
        case 'hours':
            switch (action.type) {

                case 'increment':
                    return {
                        ...state,
                        hours: Math.min(17, state.hours + 1)
                    }
                case 'decrement':
                    return {
                        ...state,
                        hours: Math.max(8, state.hours - 1)
                    }
            }

        case 'minutes':
            let newHours = state.hours
            let newMinutes = state.minutes
            switch (action.type) {

                case 'increment':
                    if (state.minutes >= 55) {
                        newHours = Math.min(17, state.hours + 1)
                        newMinutes = 0
                    } else {
                        newMinutes += 5
                    }

                    return {
                        hours: newHours,
                        minutes: newMinutes
                    }

                case 'decrement':
                    if (state.minutes <= 0) {
                        newHours = Math.max(8, state.hours - 1)
                        newMinutes = 55
                    } else {
                        newMinutes -= 5
                    }

            }
            return {
                hours: newHours,
                minutes: newMinutes
            }
    }

    if (action.type === "update") {
        return {
            hours: action.field.hours,
            minutes: action.field.minutes,
        }
    }

    return state
}

interface DeliveryForm {
    checkAmount: number,
    handleFormStep: (step: "next" | "back") => void
}


export const DeliveryForm: React.FC<DeliveryForm> = ({
    checkAmount, handleFormStep
}) => {

    const [deliveryData, setDeliveryData] = useState({
        deliveryTime: "asap",
        delivery: "delivery"
    })

    const [currentUserLocation, setCurrentUserLocation] = useState({
        street: "",
        home: "",
        homeNumber: "",
        isGetFromServer: false
    })

    const [isWarning, setIsWarning] = useState(false)

    const t = useTranslations("paydesk.thirdForm")

    useEffect(() => {
        const savedData = Cookies.get("deliveryData")
        const savedLocationData = Cookies.get("userLocation")

        if (savedData) { setDeliveryData(JSON.parse(savedData)) }

        if (savedLocationData) setCurrentUserLocation(JSON.parse(savedLocationData))

    }, [])

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.value === "selectTime") {

            const currentTime = new Date()

            currentTime.setHours(currentTime.getHours() + 1)
            const firstTime = currentTime.toLocaleTimeString("pl-PL", {
                hour: "2-digit",
                minute: "2-digit"
            })

            setDeliveryData((prev) => ({
                ...prev,
                deliveryTime: firstTime
            }))

        } else {

            setDeliveryData((prev) => ({
                ...prev,
                [e.target.name]: e.target.value,
                deliveryTime: e.target.value === "asap" ? "asap" : prev.deliveryTime
            }))
        }
    }


    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()

        const cookiesData = Cookies.get("userContactData")
        const userContactData = JSON.parse(cookiesData || "")

        const basket: BasketProps = JSON.parse(localStorage.getItem("basket") || '{}')

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

        const orderData = {
            "name": userContactData.fullName,
            "phone_number": userContactData.phone,
            "email": userContactData.email,
            "total_amount": checkAmount,
            "items": productsData,
            "delivery_time": deliveryData.deliveryTime,
            "delivery_method": deliveryData.delivery,
            "location": {
                "street": currentUserLocation.street,
                "home": currentUserLocation.home,
                "homeNumber": currentUserLocation.homeNumber
            }
        }


        Cookies.set("orderData", JSON.stringify(orderData), { expires: 14 })
        Cookies.set("deliveryData", JSON.stringify(deliveryData), { expires: 14 })
        Cookies.set("userLocation", JSON.stringify(currentUserLocation), { expires: 14 })

        handleFormStep("next")
    }

    const handleUserLocation = useCallback((inputData: locationProps | React.ChangeEvent<HTMLInputElement>): void => {
        if ("target" in inputData) {
            const { name, value } = inputData.target as HTMLInputElement
            setCurrentUserLocation((prev) => ({
                ...prev,
                [name]: value
            }))
        } else {
            setCurrentUserLocation((prev) => ({
                ...prev,
                street: inputData.street,
                home: inputData.home ? inputData.home : "",
                isGetFromServer: true
            }))
        }
    }, [])

    const getUserLocation = useCallback(async () => {
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const data = {
                    lat: position.coords.latitude,
                    long: position.coords.longitude
                }

                try {
                    const url = process.env.NEXT_PUBLIC_BACKEND_API_URL
                    const apiUrl = new URL("order/get_location", url).href
                    const response = await fetch(apiUrl, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(data)
                    })

                    if (!response.ok) {
                        throw new Error(`Failed to send/get location from ${apiUrl}`)
                    }

                    const userLocation = await response.json()
                    handleUserLocation(userLocation)

                } catch (error) {
                    console.log('Error getting location:', error)
                }
            }
        )
    }, [handleUserLocation])



    // const selectTimeTable = useMemo(() => {
    //     const currentTime = new Date()

    //     currentTime.setHours(currentTime.getHours() + 1)
    //     const firstTime = currentTime.toLocaleTimeString("pl-PL", {
    //         hour: "2-digit",
    //         minute: "2-digit"
    //     })

    //     const times: string[] = [firstTime]

    //     while (currentTime.getHours() < 20) {
    //         currentTime.setHours(currentTime.getHours() + 1)
    //         currentTime.setMinutes(0)
    //         times.push(currentTime.toLocaleTimeString("pl-PL", {
    //             hour: "2-digit",
    //             minute: "2-digit"
    //         }))
    //     }

    //     const selectDeliveryTime = (time: string) => {
    //         setDeliveryData((prev) => ({
    //             ...prev,
    //             deliveryTime: time
    //         }))
    //     }

    //     return (
    //         <div
    //             aria-hidden={deliveryData.deliveryTime === "asap"}
    //             className={clsx(styles.selectTimeContainer, { [styles.visible]: deliveryData.deliveryTime !== "asap" })
    //             }
    //         >
    //             <legend className={styles.selectedTimeTitle}>Select delivery time:</legend>
    //             <ul
    //                 aria-hidden={deliveryData.deliveryTime === "asap"}
    //                 className={styles.timeList}>
    //                 {times.map((time, index) => (
    //                     <li key={index}>
    //                         <button
    //                             aria-hidden={deliveryData.deliveryTime === "asap"}
    //                             type='button'
    //                             onClick={() => {
    //                                 selectDeliveryTime(time)
    //                             }}
    //                             className={clsx(styles.singleTimeSelectorBtn, { [styles.selected]: deliveryData.deliveryTime === time })}
    //                         >
    //                             {time}
    //                         </button>
    //                     </li>
    //                 ))}
    //             </ul>
    //         </div >
    //     )
    // }, [deliveryData])

    const [deliveryTimeData, deliveryDataDispatcher] = useReducer(Dispatcher, {
        hours: 0,
        minutes: 0
    })

    useEffect(() => {
        const now = new Date()
        const currentHour = now.getHours()
        let currentMinutes = now.getMinutes()

        currentMinutes = Math.ceil(currentMinutes / 5) * 5

        deliveryDataDispatcher({
            type: "update",
            field: {
                hours: currentHour,
                minutes: currentMinutes,
            }
        })

    }, [])

    return (
        <>
            <div className={styles.titleArea}>
                <div className={styles.title}>
                    <span>{t("title")}</span>
                    <Image src={'/icons/under-line.png'} alt={''} width={200} height={10} />
                </div>
            </div>
            <form
                // onSubmit={handleSubmit} 
                className={styles.regularForm}>

                <fieldset className={styles.deliverySection}>
                    <div className={styles.sectionSubheading}>
                        <legend>{t("Time.title")}</legend>
                    </div>
                    <div className={styles.formInputGroup}>
                        <div className={styles.inputContainer}>
                            <label className={styles.radioLabelForm} htmlFor="asap">
                                <input
                                    type="radio"
                                    id="asap"
                                    name="deliveryTime"
                                    value="asap"
                                    className={styles.radioInputForm}
                                    checked={deliveryData.deliveryTime === "asap"}
                                    onChange={handleChange}
                                />
                                {t("Time.firstInputText")}
                            </label>
                        </div>

                        <div className={styles.inputContainer}>

                            <label className={styles.radioLabelForm} htmlFor="selectTime">
                                <input
                                    type="radio"
                                    id="selectTime"
                                    name="deliveryTime"
                                    value="selectTime"
                                    className={styles.radioInputForm}
                                    checked={deliveryData.deliveryTime !== "asap"}
                                    onChange={handleChange}
                                />
                                {t("Time.secondInputText")}
                            </label>
                        </div>
                        {/* {selectTimeTable} */}
                        <div
                            aria-hidden={deliveryData.deliveryTime === "asap"}
                            className={clsx(styles.selectTimeContainer, { [styles.visible]: deliveryData.deliveryTime !== "asap" })
                            }
                        >
                            <legend className={styles.selectedTimeTitle}>
                                {t("Time.textHint")}
                            </legend>
                            <TimePeakier timeData={deliveryTimeData} setTimeData={deliveryDataDispatcher} />
                        </div>

                    </div>
                </fieldset>

                <fieldset className={styles.deliverySection}>
                    <div className={styles.sectionSubheading}>
                        <legend>{t("Delivery.title")}</legend>
                    </div>
                    <div className={styles.formInputGroup}>
                        <div className={styles.inputContainer}>
                            <label
                                className={clsx(styles.radioLabelForm)} htmlFor="delivery">
                                <input
                                    type='radio'
                                    id='delivery'
                                    name='delivery'
                                    value='delivery'
                                    checked={deliveryData.delivery === "delivery"}
                                    onChange={handleChange}
                                    placeholder=''
                                    required
                                    className={styles.radioInputForm}
                                />
                                {t("Delivery.firstInputText")}
                            </label>
                        </div>
                        <div className={styles.inputContainer}>
                            <label className={clsx(styles.radioLabelForm)} htmlFor="contactless delivery">
                                <input
                                    type='radio'
                                    id='contactless delivery'
                                    name='delivery'
                                    value='contactless delivery'
                                    checked={deliveryData.delivery === "contactless delivery"}
                                    onChange={handleChange}
                                    placeholder=''
                                    required
                                    className={styles.radioInputForm}
                                />
                                {t("Delivery.secondInputText")}
                            </label>
                        </div>
                        <div className={styles.inputContainer}>
                            <label className={clsx(styles.radioLabelForm, styles.required)} htmlFor="own collection">
                                <input
                                    type='radio'
                                    id='own collection'
                                    name='delivery'
                                    value="own collection"
                                    checked={deliveryData.delivery === "own collection"}
                                    onChange={handleChange}
                                    placeholder=''
                                    required
                                    className={styles.radioInputForm}
                                />
                                {t("Delivery.thirdInputText")}
                            </label>
                        </div>
                    </div>
                </fieldset>

                {deliveryData.delivery !== "own" &&
                    <fieldset className={styles.deliverySection}>
                        <div className={styles.sectionSubheading}>
                            <legend>
                                {t("Location.title")}
                            </legend>
                        </div>
                        <div className={styles.buttonLocation}>
                            <button type='button' onClick={() => {
                                getUserLocation()
                                setIsWarning(true)

                                setTimeout(() => setIsWarning(false), 50)
                            }} >
                                {t("Location.locateButton")}
                            </button>
                        </div>
                        {currentUserLocation.isGetFromServer &&
                            <motion.p
                                className={styles.warningLocationText}
                                animate={isWarning ?
                                    {
                                        color: ["#ff0000", "#000"]
                                    } :
                                    {
                                        color: "#ff0000"
                                    }
                                }
                                transition={{
                                    duration: 1,
                                    repeat: Infinity,
                                    ease: "easeInOut"
                                }}

                            >
                                {t("Location.textHint")}
                            </motion.p>
                        }
                        <div className={styles.formInputGroup}>
                            <div className={styles.inputContainer}>
                                <input
                                    type='text'
                                    id='street'
                                    name='street'
                                    value={currentUserLocation.street}
                                    onChange={handleUserLocation}
                                    placeholder=''
                                    required
                                    className={styles.regularInputForm}
                                ></input>
                                <label className={clsx(styles.regularLabelForm, styles.required)} htmlFor="Street">
                                    {t("Location.firstInputText")}
                                </label>
                            </div>
                            <div className={styles.inputContainer}>
                                <input
                                    type='text'
                                    id='home'
                                    name='home'
                                    value={currentUserLocation.home}
                                    onChange={handleUserLocation}
                                    placeholder=''
                                    required
                                    className={styles.regularInputForm}
                                ></input>
                                <label className={clsx(styles.regularLabelForm, styles.required)} htmlFor="home">
                                    {t("Location.secondInputText")}
                                </label>
                            </div>
                            <div className={styles.inputContainer}>
                                <input
                                    type='text'
                                    id='homeNumber'
                                    name='homeNumber'
                                    value={currentUserLocation.homeNumber}
                                    onChange={handleUserLocation}
                                    placeholder=''
                                    className={styles.regularInputForm}
                                ></input>
                                <label className={clsx(styles.regularLabelForm)} htmlFor="homeNumber">
                                    {t("Location.thirdInputText")}
                                </label>
                            </div>
                        </div>
                    </fieldset>
                }

                <div className={styles.submitSegmentBtn}>
                    <button
                        className={styles.prevBtn}
                        type='button'
                        onClick={() => handleFormStep('back')}
                    >
                        Back
                    </button>
                    <button
                        className={styles.nextBtn}
                        onClick={handleSubmit}
                    >
                        {t("submitButton")}
                    </button>
                </div>

            </form>
        </>
    )
}