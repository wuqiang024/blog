/*
 * @Author: wuqiang
 * @Date: 2022-06-15 11:38:03
 * @LastEditors: wuqiang
 * @LastEditTime: 2022-06-15 13:15:48
 */
export function typeOf(obj) {
  return Object.prototype.toString.call(obj).slice(8, -1).toLowerCase()
}

export function shallowCopy(obj) {
  if(!typeOf(obj) !== 'object' || !typeOf(obj) !== 'array') return obj;
  const result = typeOf(obj) !== 'object' ? [] : {};
  for(let key in obj) {
    result[key] = obj[key]
  }
}

export function renderTemplate(template, data) {
  const pattern = /\{\{(\w+)\}\}/;
  if(pattern.test(template)) {
    const name = pattern.exec(template)[1];
    template = template.replace(pattern, data[name]);
    return renderTemplate(template, data);
  }
  return template;
}