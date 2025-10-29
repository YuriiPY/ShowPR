import clsx from 'clsx'
import Cookies from "js-cookie"
import { ShieldAlert } from 'lucide-react'
import { useTranslations } from 'next-intl'
import Image from 'next/image'
import React, { useEffect, useState } from 'react'


import styles from './UserDataForm.module.scss'

interface FirstFormProps {
    handleFormStep: (step: "next" | "back") => void
}
type userDataProps = {
    fullName: string
    email: string
    phone: string
    verificationState: boolean
    verify: boolean
}

type VerifyFormProps = {
    userData: userDataProps
    setLocalData: React.Dispatch<React.SetStateAction<userDataProps>>
    handleFormStep: (step: "next" | "back") => void
}

export const UserDataForm: React.FC<FirstFormProps> = ({ handleFormStep }) => {

    const t = useTranslations("paydesk.firstForm")

    const [userData, setUserData] = useState<userDataProps>({
        fullName: "",
        email: "",
        phone: "",
        verificationState: false,
        verify: false
    })

    useEffect(() => {
        const savedData = Cookies.get("userContactData")

        if (savedData) {
            const userCookieData = JSON.parse(savedData)
            setUserData((prev) => ({
                ...prev,
                ...userCookieData
            }))
            handleFormStep("next")

        }
    }, [handleFormStep])

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target
        setUserData((prev) => ({
            ...prev,
            [name]: value
        }))
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()

        if (userData.verify) {
            Cookies.set("userContactData", JSON.stringify(userData), { expires: 14 })
            handleFormStep("next")
        } else {
            setUserData((prev) => ({
                ...prev,
                verificationState: true
            }))
        }
        handleFormStep("next")
    }

    return (
        <>
            {!userData.verificationState ?
                <>
                    <div className={styles.titleArea}>
                        <div className={styles.title}>
                            <span>{t("title")}</span>
                            <Image src={'/icons/under-line.png'} alt={''} width={200} height={10} />
                        </div>
                    </div>
                    <form onSubmit={handleSubmit} className={styles.regularForm}>
                        <div className={styles.inputContainer}>
                            <input
                                type='text'
                                id='fullName'
                                name='fullName'
                                value={userData.fullName}
                                onChange={handleChange}
                                placeholder=''
                                required
                                className={styles.regularInputForm}
                            ></input>
                            <label className={clsx(styles.regularLabelForm, styles.required)} htmlFor="fullName">{t("firstInputText")}</label>
                        </div>
                        <div className={styles.inputContainer}>
                            <input
                                type='email'
                                id='email'
                                name='email'
                                value={userData.email}
                                onChange={handleChange}
                                placeholder=''
                                required
                                className={styles.regularInputForm}
                            ></input>
                            <label className={styles.regularLabelForm} htmlFor="email">{t("secondInputText")}</label>
                        </div>
                        <div className={styles.inputContainer}>
                            <input
                                type='tel'
                                id='phone'
                                name='phone'
                                value={userData.phone}
                                onChange={handleChange}
                                placeholder=''
                                required
                                className={styles.regularInputForm}
                            ></input>
                            <label className={clsx(styles.regularLabelForm, styles.required)} htmlFor="phone">{t("thirdInputText")}</label>
                        </div>
                        <div className={styles.submitBtn}>
                            <button>{t("submitButton")}</button>
                        </div>
                    </form>
                </>
                :
                <VerifyForm userData={userData} setLocalData={setUserData} handleFormStep={handleFormStep} />
            }

        </>
    )
}

export const VerifyForm = ({ userData, setLocalData, handleFormStep }: VerifyFormProps) => {
    // const [verifyCode, setVerifyCode] = useState("")

    const t = useTranslations("paydesk.secondForm")

    //FIXME:
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target)
            // const { name, value } = e.target
            // setVerifyCode(value)
            setLocalData((prev) => ({
                ...prev,
                verify: true
            }))
    }

    const { ...newUserData } = userData

    // TODO: CREATE VERIFICATION FUNCTION 
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()

        //FIXME: DO NOT SAVE USER DATA WHEN SENT DATA ON SERVER  
        Cookies.set("userContactData", JSON.stringify(newUserData), { expires: 14 })


        handleFormStep("next")
    }

    return (
        <>
            <div className={styles.titleArea}>
                <div className={styles.title}>
                    <span>{t("title")}</span>
                    <Image src={'/icons/under-line.png'} alt={''} width={200} height={10} />
                </div>
            </div>
            <form onSubmit={handleSubmit} className={styles.regularForm}>
                <ShieldAlert size={30} color='#84ffa7' />
                <p>{t("textHint")}</p>
                <div className={styles.inputContainer}>
                    <input
                        type='text'
                        id='verify'
                        name='verify'
                        onChange={handleChange}
                        placeholder=''
                        required
                        className={styles.regularInputForm}
                    ></input>
                    <label className={styles.regularLabelForm} htmlFor="verifyPhone">{t("inputText")}</label>
                </div>
                <div className={styles.submitBtn}>
                    <button>{t("submitButton")}</button>
                </div>
            </form>

        </>
    )
}