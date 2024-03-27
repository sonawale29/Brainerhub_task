# In views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .models import Employee, Company
from .serializers import EmployeeSerializer,CompanySerializer

class UploadExcel(APIView):

    def post(self, request, format=None):
        # Check if a file was provided in the request
        if 'file' not in request.FILES:
            return Response({'error': 'No file was provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(file)

            # Retrieve or create Company instances for each unique company name
            company_names = df['COMPANY_NAME'].unique()
            companies = {}
            for name in company_names:
                company_instance = Company.objects.filter(company_name=name).first()
                if company_instance is None:
                    company_instance = Company.objects.create(company_name=name)
                companies[name] = company_instance

            # Replace company names in the DataFrame with their corresponding primary keys
            df['company_name'] = df['COMPANY_NAME'].map(lambda name: companies[name].pk)

            # Rename columns to match the field names in the Employee model
            df.rename(columns={
                'EMPLOYEE_ID': 'employee_id',
                'FIRST_NAME': 'first_name',
                'LAST_NAME': 'last_name',
                'PHONE_NUMBER': 'phone_number',
                'SALARY': 'salary',
                'MANAGER_ID': 'manager_id',
                'DEPARTMENT_ID': 'department_id',
                'COMPANY_NAME': 'company_name'
            }, inplace=True)

            # Convert DataFrame to list of dictionaries
            employee_data = df.to_dict(orient='records')

            # Initialize the serializer with many=True
            serializer = EmployeeSerializer(data=employee_data, many=True)

            # Check if serializer data is valid
            if serializer.is_valid():
                # Save the data to the database
                serializer.save()
                return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
            else:
                # Return serializer errors if data is not valid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Return error if an exception occurs
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeCompanyAPIView(APIView):
    def get(self, request, format=None):
        employees = Employee.objects.all()  # Get all employees
        serializer = EmployeeSerializer(employees, many=True)  # Serialize employee data
        return Response(serializer.data)  # Return serialized employee data
