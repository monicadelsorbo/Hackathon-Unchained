import { useState, useEffect, useCallback } from 'react'

export function usePolling<T>(
  fetchFn: () => Promise<T>,
  intervalMs: number = 2000,
  enabled: boolean = true
) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  const refetch = useCallback(async () => {
    try {
      const result = await fetchFn()
      setData(result)
      setError(null)
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [fetchFn])

  useEffect(() => {
    if (!enabled) return

    refetch()
    const id = setInterval(refetch, intervalMs)
    return () => clearInterval(id)
  }, [refetch, intervalMs, enabled])

  return { data, error, loading, refetch }
}
