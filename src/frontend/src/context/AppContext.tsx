import { createContext, useContext, useState, ReactNode } from 'react'

interface AppContextType {
  appName: string
  soundEnabled: boolean
  setAppName: (name: string) => void
  setSoundEnabled: (enabled: boolean) => void
}

const AppContext = createContext<AppContextType>({
  appName: 'SignalShop',
  soundEnabled: true,
  setAppName: () => {},
  setSoundEnabled: () => {},
})

export function AppProvider({ children }: { children: ReactNode }) {
  const [appName, setAppName] = useState('SignalShop')
  const [soundEnabled, setSoundEnabled] = useState(true)

  return (
    <AppContext.Provider value={{ appName, soundEnabled, setAppName, setSoundEnabled }}>
      {children}
    </AppContext.Provider>
  )
}

export function useAppContext() {
  return useContext(AppContext)
}