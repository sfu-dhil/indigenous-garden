const assets = JSON.parse(document.getElementById('garden-features-data').textContent).reduce((result, o) => result.set(o.id, o), new Map())

export const useData = () => {
  return {

  } = assets
}