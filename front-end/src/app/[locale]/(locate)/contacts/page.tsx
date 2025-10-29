'use client'

import { Mail, MapPin, Phone } from 'lucide-react'
import Image from 'next/image'
import Iframe from 'react-iframe'

import Header from '@/components/Header/Header/Header'
import HoursTable from '@/components/HoursTable/HoursTable'
import { useTranslations } from 'next-intl'
import { useState } from 'react'
import styles from './Contacts.module.scss'



export default function MainPage() {
    const [showMap, setShowMap] = useState(0)
    const t = useTranslations("ContactsPage")

    const handleChangeSelector = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setShowMap(Number(event.target.value))
    }

    const openHoursList = [
        { "day": t("Information.workDays.mon"), "hours": "8:00-17:00" },
        { "day": t("Information.workDays.tue"), "hours": "8:00-17:00" },
        { "day": t("Information.workDays.wed"), "hours": "8:00-17:00" },
        { "day": t("Information.workDays.thu"), "hours": "8:00-17:00" },
        { "day": t("Information.workDays.fri"), "hours": "8:00-17:00" },
        { "day": t("Information.workDays.sat"), "hours": "8:00-15:00" },
        { "day": t("Information.workDays.sun"), "hours": t("Information.closed") }
    ]

    const deliveryHoursList = [
        { "day": t("Information.workDays.mon"), "hours": "8:00-16:00" },
        { "day": t("Information.workDays.tue"), "hours": "8:00-16:00" },
        { "day": t("Information.workDays.wed"), "hours": "8:00-16:00" },
        { "day": t("Information.workDays.thu"), "hours": "8:00-16:00" },
        { "day": t("Information.workDays.fri"), "hours": "8:00-16:00" },
        { "day": t("Information.workDays.sat"), "hours": "8:00-14:00" },
        { "day": t("Information.workDays.sun"), "hours": t("Information.closed") }
    ]

    return (
        <div>
            <Header dataImg={'/Menu/background/bg.jpg'} isActiveHeader={'off'} isButton={'off'} />
            <section className={styles.mainContact}>
                <div >
                    <div className={styles.subheader}>
                        <h2 className={styles.heading}>
                            <span className={styles.title}>{t("title1")}</span>
                            <span className={styles.subTitle}>{t("title2")}</span>
                        </h2>
                        <p>{t("title3")}</p>
                    </div>
                    <div className={styles.chooseBase}>
                        <div className={styles.chooseGroup}>
                            <label className={styles.selectRestaurant}>{t("selectorLabel")}</label>
                            <span className={styles.mSelect}>
                                <select className={styles.selector} onChange={handleChangeSelector}>
                                    <option value={"0"}>Alina Pierogowa Oleśnicka 13</option>
                                    <option value={"1"}>Alina Pierogowa Stefana Czarnieckiego 29a</option>
                                </select>
                            </span>
                        </div>
                    </div>
                    <div className={styles.allInfo}>
                        <div className={styles.contactData}>
                            <div className={styles.contactItem}>
                                <h3 className={styles.title}>{t("Information.addressTitle")}</h3>
                                <div className={styles.icon}>
                                    <Image src={'/icons/under-line.png'} alt={''} width={100} height={10} />
                                </div>
                                <address>
                                    <ul className={styles.listVertical}>
                                        <li className={styles.listVerticalLi} >
                                            <div className={styles.listIcon}>
                                                <MapPin />
                                            </div>
                                            <span>Oleśnicka 13</span>
                                            <span>50-320 Wrocławs</span>
                                        </li>
                                        <li className={styles.listVerticalLi}>
                                            <div className={styles.listIcon}>
                                                <Phone />
                                            </div>
                                            <span>731 307 087</span>
                                        </li >
                                        <li className={styles.listVerticalLi} >
                                            < div className={styles.listIcon}>
                                                < Mail />
                                            </div >
                                            <a href="styles.https//mail.google.com/mail/u/0/#inbox?compose=CllgCJZcRPQdGPsrkDnQCwBGtLDNkZPqnJspJjNlNVVTKzgKkCjPMmFJJlBxmTZPCsmVqJbJzdq">
                                                <span>alina_pierogowa@gmail.com</span>
                                            </a >
                                        </li >
                                    </ul >
                                </address >
                                <br></br>
                                <div className={styles.timeLimitsContainer}>
                                    <HoursTable title={t("Information.openHours")} rows={openHoursList} />
                                    <HoursTable title={t("Information.deliveryHours")} rows={deliveryHoursList} />
                                </div >
                            </div >
                        </div >
                        <div className={styles.maps}>
                            <div className={styles.contactMap}>

                                <div className="firstMap" style={{ display: showMap === 0 ? "block" : "none" }}>
                                    <Iframe
                                        url={'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2504.3207190393746!2d17.04197507707197!3d51.120991971728!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x470fe9f9a1132313%3A0x55b3d3ff7d2b4304!2sAlina%20Pierogowa!5e0!3m2!1sru!2spl!4v1737844067809!5m2!1sru!2spl'}
                                        width="600px"
                                        height="450px"
                                        id=""
                                        allowFullScreen
                                        loading="lazy"
                                    />
                                </div >
                                <div style={{ display: showMap === 1 ? "block" : "none" }}>
                                    <Iframe
                                        url={'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2504.5868397691875!2d17.003374177071702!3d51.11608267172697!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x470fe958e6994147%3A0xa980d1fcf992200f!2sAlina%20Pierogowa!5e0!3m2!1sru!2spl!4v1737889359803!5m2!1sru!2spl '}
                                        width="600px"
                                        height="450px"
                                        id=""
                                        allowFullScreen
                                        loading="lazy"
                                    />
                                </div >
                            </div >
                        </div >
                    </div >
                </div >
            </section >
        </div >
    )
}	