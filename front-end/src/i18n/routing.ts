import { defineRouting } from 'next-intl/routing'

export const routing = defineRouting({
    locales: ['en', 'ua', 'pl'],
    defaultLocale: 'pl'
})