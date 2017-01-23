import { schema } from 'normalizr';

const urlSchema = new schema.Entity('data')
const sitesSchema = new schema.Array(urlSchema)

export { sitesSchema }
