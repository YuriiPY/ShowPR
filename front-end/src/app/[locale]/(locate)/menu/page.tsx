'use client'

import Header from '@/components/Header/Header/Header'
import MainMenu from '@/components/MenuComponents/MainMenu/MainMenu'

export default function MainPage() {
    return (
        <div>
            <Header dataImg={'/Menu/background/bg.jpg'} isActiveHeader={'off'} isButton={'off'} />
            <MainMenu />
        </div>
    )
}	