
//环境代理监控
function setProxy(proxyObjArr) {
    for (let i = 0; i < proxyObjArr.length; i++) {
        const objName = proxyObjArr[i];
        const handler = {
            get(target, property, receiver) {
                console.log("方法:", "get", ",对象:", objName, ",对象属性:", property, ",属性类型:", typeof property, ",属性值:", target[property], ",属性值类型:", typeof target[property]);
                return target[property];
            },

            set(target, property, value, receiver) {
                console.log("方法:", "set", ",对象:", objName, ",对象属性:", property, ",属性类型:", typeof property, ",属性值:", target[property], ",属性值类型:", typeof target[property]);
                return Reflect.set(target, property, value, receiver)
            }
        }
        let targetObject = global[objName];
        global[objName] = new Proxy(targetObject, handler);
    }
}

setProxy(["window", "navigator","document","location", "localStorage", "history", "element"])