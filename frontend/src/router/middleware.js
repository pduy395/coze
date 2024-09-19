export async function loadLayoutMiddleware(route) {
  try {
      let layout = route.meta.layout.__name
      // route.meta.layoutComponent = layout.default
      // console.log(layout)
  } catch (e) {
      console.error('Error occurred in processing of layouts: ', e)
      let layout = 'DefaultLayout'
      let layoutComponent = await import(`@/layouts/${layout}.vue`)
      route.meta.layoutComponent = layoutComponent.default
      console.log(layoutComponent)
  }
}