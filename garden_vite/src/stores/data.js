const featureMap = JSON.parse(document.getElementById('garden-features-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const points = [...featureMap.values()].reduce((result, o) => result.concat(o.points.map((p) => ({...p, featureId: o.id}))), [])

export const useData = () => {
  return {
    featureMap,
    points,
  }
}