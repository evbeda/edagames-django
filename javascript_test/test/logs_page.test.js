const app = require('../../static/js/logs_page');

describe("Transform TEXT to JSON" , ()=>{  
    test("transform test message" , ()=>{
        const test_message = `{
            'test':'im test',
            'test_object':{
                'data':"Hello im data"
            }
        }`;
        const test_json_array = [{
            "test":"im test",
            "test_object":{
                "data":"Hello im data"
            }
        }]
        app.addLogToArray(test_message)
        expect(app.listOfLogs).toEqual(test_json_array);
    })
})
